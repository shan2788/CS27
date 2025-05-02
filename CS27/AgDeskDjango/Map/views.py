from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.conf import settings

import os, json, requests, datetime, logging, joblib, torch, hashlib, base64
import matplotlib.pyplot as plt
import numpy as np
import asyncio, aiohttp
from io import BytesIO
from collections import defaultdict

from .models import NDVIRegion, NDVIReport, CarbonCredit
from FarmAcc.models import FarmInfo
from .sentinel_auth import get_sentinel_token, get_sentinel_instance_id
from .services.prediction_service import CropModelService, BiomassModelService, convert_tree_biomass_array_to_CO2
from .utils import (
    generate_pdf_report, are_geometries_similar, generate_credit_report,
    calculate_area_square
)
from .test_pre import make_tree_recommendation, make_density_prediction, fake_carbon_series

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATHS = {
    'crop_model': os.path.join(BASE_DIR, "rf_model.pkl"),
    'crop_encoder': os.path.join(BASE_DIR, "label_encoder.pkl"),
    'biomass_model': os.path.join(BASE_DIR, "biomass_model.pkl"),
    'scaler_X': os.path.join(BASE_DIR, 'scaler_X.pkl'),
    'scaler_y': os.path.join(BASE_DIR, 'scaler_y.pkl'),
    'cache_dir': os.path.join(BASE_DIR, "cache"),
    'cache_index': os.path.join(BASE_DIR, "cache_index.json")
}
REPORT_PATH = os.path.join(settings.MEDIA_ROOT, "report")

NDVI_EVALSCRIPT = """//VERSION=3
function setup() {
  return { input: ["B04", "B08"], output: { bands: 4, sampleType: "UINT8" }};
}
function evaluatePixel(sample) {
  let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
  let r=0,g=0,b=0,a=255;
  if (ndvi < -0.2) r=g=b=0;
  else if (ndvi < 0) { r=165; g=42; b=42; }
  else if (ndvi < 0.2) { r=255; g=255; b=0; }
  else if (ndvi < 0.4) { r=0; g=255; b=0; }
  else { r=0; g=128; b=0; }
  if (sample.B08 === 0 && sample.B04 === 0) a = 0;
  return [r, g, b, a];
}"""

@login_required(login_url="login")
def map_view(request):
    return render(request, 'Map/map.html', {"sentinel_instance_id": get_sentinel_instance_id()})

# ------------------ Utility: fetch NDVI image ------------------

async def get_ndvi_image_binary(session, geometry, start_date, end_date, evalscript, use_cache=True):
    cache_key = hashlib.md5(f"{geometry}_{start_date}_{end_date}".encode()).hexdigest()
    cache_path = os.path.join(MODEL_PATHS['cache_dir'], f"{cache_key}.png")
    cache_index = {}

    # Read cache index
    if use_cache and os.path.exists(MODEL_PATHS['cache_index']):
        with open(MODEL_PATHS['cache_index'], "r") as f:
            cache_index = json.load(f)
        for cached_key, cached_data in cache_index.items():
            if are_geometries_similar(geometry, cached_data["geometry"], threshold=0.8):
                logger.info("Async cache hit based on geometry similarity.")
                cached_file = cached_data["cache_path"]
                if os.path.exists(cached_file):
                    with open(cached_file, "rb") as f:
                        return f.read()

    # Sentinel Hub request payload
    payload = {
        "input": {
            "bounds": {"geometry": geometry},
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": f"{start_date}T00:00:00Z",
                        "to": f"{end_date}T23:59:59Z"
                    }
                }
            }]
        },
        "output": {
            "width": 512,
            "height": 512,
            "responses": [{
                "identifier": "default",
                "format": {"type": "image/png"}
            }]
        },
        "evalscript": evalscript
    }

    headers = {
        "Authorization": f"Bearer {get_sentinel_token()}",
        "Content-Type": "application/json"
    }

    try:
        async with session.post("https://services.sentinel-hub.com/api/v1/process", headers=headers, json=payload, timeout=30) as resp:
            if resp.status == 200:
                image_data = await resp.read()
                if use_cache:
                    os.makedirs(MODEL_PATHS['cache_dir'], exist_ok=True)
                    with open(cache_path, "wb") as f:
                        f.write(image_data)
                    cache_index[cache_key] = {"geometry": geometry, "cache_path": cache_path}
                    with open(MODEL_PATHS['cache_index'], "w") as f:
                        json.dump(cache_index, f)
                    logger.info("NDVI image saved to async cache.")
                return image_data
            else:
                logger.warning(f"Async Sentinel error {resp.status}: {await resp.text()}")
    except asyncio.TimeoutError:
        logger.error("Request to Sentinel timed out.")
    except Exception as e:
        logger.error(f"Async error in NDVI fetch: {e}")
    return None

# ------------------ View: return NDVI image (no save) ------------------

@csrf_exempt
def ndvi_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry = data['geometry']
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        async def fetch_ndvi():
            async with aiohttp.ClientSession() as session:
                return await get_ndvi_image_binary(
                    session=session,
                    geometry=geometry,
                    start_date=start_date,
                    end_date=end_date,
                    evalscript=NDVI_EVALSCRIPT,
                    use_cache=False
                )

        image_data = asyncio.run(fetch_ndvi())
        if image_data:
            return HttpResponse(image_data, content_type="image/png")
        return JsonResponse({'error': 'No image returned'}, status=500)

    except Exception as e:
        logger.error("NDVI preview error: " + str(e))
        return JsonResponse({'error': str(e)}, status=400)



# ------------------ Utility: save NDVI image to database ------------------

def save_ndvi_image_to_region(farm, geometry_data, image_binary):
    geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)
    region = NDVIRegion(farm=farm, geometry=geo_obj)
    filename = f"ndvi_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    region.image.save(filename, ContentFile(image_binary))
    region.save()
    return region.id

# ------------------ View: save NDVI result ------------------

@csrf_exempt
def save_ndvi_result(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        current_user = request.user
        farm_id = current_user.currentFarm_id
        data = json.loads(request.body)

        geometry_data = data['geometry']
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        async def fetch_and_save():
            async with aiohttp.ClientSession() as session:
                image_binary = await get_ndvi_image_binary(
                    session=session,
                    geometry=geometry_data,
                    start_date=start_date,
                    end_date=end_date,
                    evalscript=NDVI_EVALSCRIPT,
                    use_cache=True
                )
                if not image_binary:
                    return None
                farm = FarmInfo.objects.get(id=farm_id)
                return save_ndvi_image_to_region(farm, geometry_data, image_binary)

        region_id = asyncio.run(fetch_and_save())
        if region_id:
            return JsonResponse({'status': 'ok', 'id': region_id})
        return JsonResponse({'error': 'Failed to fetch or save image'}, status=500)

    except Exception as e:
        logger.error("Error saving NDVI region: " + str(e))
        return JsonResponse({'error': str(e)}, status=400)

...

# ------------------ Utility: save NDVI image to database ------------------

def save_ndvi_image_to_region(farm, geometry_data, image_binary):
    geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)
    region = NDVIRegion(farm=farm, geometry=geo_obj)
    filename = f"ndvi_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    region.image.save(filename, ContentFile(image_binary))
    region.save()
    return region.id

# ------------------ View: save NDVI result ------------------

@csrf_exempt
def save_ndvi_result(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        current_user = request.user
        farm_id = current_user.currentFarm_id
        data = json.loads(request.body)

        geometry_data = data['geometry']
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        async def fetch_and_save():
            async with aiohttp.ClientSession() as session:
                image_binary = await get_ndvi_image_binary(
                    session=session,
                    geometry=geometry_data,
                    start_date=start_date,
                    end_date=end_date,
                    evalscript=NDVI_EVALSCRIPT,
                    use_cache=True
                )
                if not image_binary:
                    return None
                farm = FarmInfo.objects.get(id=farm_id)
                return save_ndvi_image_to_region(farm, geometry_data, image_binary)

        region_id = asyncio.run(fetch_and_save())
        if region_id:
            return JsonResponse({'status': 'ok', 'id': region_id})
        return JsonResponse({'error': 'Failed to fetch or save image'}, status=500)

    except Exception as e:
        logger.error("Error saving NDVI region: " + str(e))
        return JsonResponse({'error': str(e)}, status=400)

# ------------------ Utility: get NDVI statistics ------------------

def get_statistics_data(geometry, start_date, end_date):
    evalscript = """//VERSION=3
    function setup() {
      return {
        input: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12", "dataMask"],
        output: [
          { id: "B01", bands: 1, sampleType: "FLOAT32" },
          { id: "B02", bands: 1, sampleType: "FLOAT32" },
          { id: "B03", bands: 1, sampleType: "FLOAT32" },
          { id: "B04", bands: 1, sampleType: "FLOAT32" },
          { id: "B05", bands: 1, sampleType: "FLOAT32" },
          { id: "B06", bands: 1, sampleType: "FLOAT32" },
          { id: "B07", bands: 1, sampleType: "FLOAT32" },
          { id: "B08", bands: 1, sampleType: "FLOAT32" },
          { id: "B8A", bands: 1, sampleType: "FLOAT32" },
          { id: "B09", bands: 1, sampleType: "FLOAT32" },
          { id: "B11", bands: 1, sampleType: "FLOAT32" },
          { id: "B12", bands: 1, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      if (sample.dataMask === 0) {
        return {
          B01: [NaN], B02: [NaN], B03: [NaN], B04: [NaN], B05: [NaN], B06: [NaN], B07: [NaN],
          B08: [NaN], B8A: [NaN], B09: [NaN], B11: [NaN], B12: [NaN], dataMask: [0]
        };
      }
      return {
        B01: [sample.B01], B02: [sample.B02], B03: [sample.B03], B04: [sample.B04],
        B05: [sample.B05], B06: [sample.B06], B07: [sample.B07], B08: [sample.B08],
        B8A: [sample.B8A], B09: [sample.B09], B11: [sample.B11], B12: [sample.B12],
        dataMask: [1]
      };
    }"""

    band_ids = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"]
    stats = {band: {"statistics": ["min", "max", "mean"]} for band in band_ids}

    payload = {
        "input": {
            "bounds": {"geometry": geometry},
            "data": [{"type": "sentinel-2-l2a"}]
        },
        "aggregation": {
            "timeRange": {
                "from": f"{start_date}T00:00:00Z",
                "to": f"{end_date}T23:59:59Z"
            },
            "aggregationInterval": {"of": "P7D"},
            "width": 512,
            "height": 512,
            "evalscript": evalscript
        },
        "calculations": {"default": {"statistics": stats}}
    }

    headers = {
        "Authorization": f"Bearer {get_sentinel_token()}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://services.sentinel-hub.com/api/v1/statistics", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("data", [])
    raise Exception(f"Statistics error {response.status_code}: {response.text}")

# ------------------ Utility: process NDVI statistics into model input ------------------

def get_statistics_for_model_input(geometry, start_date, end_date):
    try:
        raw_stats = get_statistics_data(geometry, start_date, end_date)
        results = []
        for entry in raw_stats:
            interval = entry.get("interval", {})
            outputs = entry.get("outputs", {})

            bands_mean = {}
            for band_name, band_data in outputs.items():
                band_stats = band_data.get("bands", {}).get("B0", {}).get("stats", {})
                mean_val = band_stats.get("mean")
                bands_mean[band_name] = mean_val * 10000 if mean_val is not None else None

            b08 = bands_mean.get("B08")
            b04 = bands_mean.get("B04")
            ndvi = (b08 - b04) / (b08 + b04) if b08 is not None and b04 is not None and (b08 + b04) != 0 else None

            results.append({
                "from": interval.get("from"),
                "to": interval.get("to"),
                "bands_mean": bands_mean,
                "ndvi_mean": ndvi
            })

        return results

    except Exception as e:
        logger.error(f"Error processing statistics for model input: {e}")
        return []



...

# ------------------ View: generate NDVI report ------------------

@csrf_exempt
def generate_report(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry_data = data.get("geometry")
        start_date = data.get("start_date", "2025-02-23")
        end_date = data.get("end_date", "2025-03-23")

        if not geometry_data:
            return JsonResponse({'error': 'Missing geometry data'}, status=400)

        geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)

        # Step 1: 统计数据与模型输入
        formatted_data = get_statistics_for_model_input(geometry_data, start_date, end_date)

        # Step 2: 作物预测
        crop_model = CropModelService(logger, model_path=MODEL_PATHS['crop_model'], encoder_path=MODEL_PATHS['crop_encoder'])
        predicted_crop = crop_model.make_prediction(formatted_data)

        # Step 3: 生物量预测与 CO2 转换
        biomass_model = BiomassModelService(logger, model_path=MODEL_PATHS['biomass_model'], scaler_X_path=MODEL_PATHS['scaler_X'], scaler_y_path=MODEL_PATHS['scaler_y'])
        predicted_biomass = biomass_model.make_prediction(formatted_data)

        # Step 4: 报告生成与保存
        buffer = generate_pdf_report(start_date, end_date, predicted_crop, predicted_biomass, formatted_data)
        filename = f"NDVI_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(REPORT_PATH, filename)
        os.makedirs(REPORT_PATH, exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        # Step 5: 记录写入数据库
        current_user = request.user
        farm_id = getattr(current_user, "currentFarm_id", None)
        farm = FarmInfo.objects.get(id=farm_id) if farm_id else None
        NDVIReport.objects.create(
            farm=farm,
            start_date=start_date,
            end_date=end_date,
            file_path=f'report/{filename}',
            geolocation=geo_obj
        )

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ------------------ View: tree recommendation & carbon forecast ------------------

@csrf_exempt
def tree_recommendation_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry = data.get('geometry')
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        # 统计数据转换为模型输入
        formatted_data = get_statistics_for_model_input(geometry, start_date, end_date)
        if not formatted_data:
            return JsonResponse({'error': 'No NDVI stats available'}, status=400)

        # 树种推荐与密度估计
        species = make_tree_recommendation(formatted_data)
        density = make_density_prediction(formatted_data)
        carbon_list = fake_carbon_series(density)
        years = [str(2025 + i) for i in range(len(carbon_list))]

        # 绘制碳变化图表
        plt.figure()
        plt.plot(years, carbon_list, marker='o')
        plt.title("Predicted Carbon Change")
        plt.xlabel("Year")
        plt.ylabel("Carbon Emission (ton/year)")
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()

        # 返回 HTML 片段供 HTMX 局部替换
        html = render_to_string("Map/tree_result_fragment.html", {
            "species": species,
            "density": density,
            "carbon": chart_base64,
        })
        return HttpResponse(html)

    except Exception as e:
        logger.error(f"Error in tree_recommendation_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# ------------------ View: NDVI monthly summary ------------------

@csrf_exempt
def ndvi_monthly_summary(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry = data['geometry']
        start_date = data['start_date']
        end_date = data['end_date']
        weekly_stats = get_statistics_for_model_input(geometry, start_date, end_date)
        if not weekly_stats:
            return JsonResponse({'error': 'No weekly data found'}, status=404)
        # 聚合到每月
        monthly_data = defaultdict(list)
        for entry in weekly_stats:
            date_obj = datetime.datetime.fromisoformat(entry["from"][:10])
            month_key = date_obj.strftime("%Y-%m")
            monthly_data[month_key].append(entry)
        month_meta = []
        month_tasks = []
        for month, entries in monthly_data.items():
            ndvi_vals = [e["ndvi_mean"] for e in entries if e["ndvi_mean"] is not None]
            if not ndvi_vals:
                continue
            mean_ndvi = round(np.mean(ndvi_vals), 3)
            max_ndvi = round(np.max(ndvi_vals), 3)
            min_ndvi = round(np.min(ndvi_vals), 3)
            mid_entry = entries[len(entries) // 2]
            mid_from = mid_entry["from"][:10]
            mid_to = mid_entry["to"][:10]

            month_meta.append((month, mean_ndvi, max_ndvi, min_ndvi))
            month_tasks.append((geometry, mid_from, mid_to, NDVI_EVALSCRIPT))

        async def fetch_all_images():
            results = []
            async with aiohttp.ClientSession() as session:
                responses = await asyncio.gather(*[
                    get_ndvi_image_binary(session, g, s, e, script, use_cache=False)
                    for g, s, e, script in month_tasks
                ])
                for i, image_blob in enumerate(responses):
                    month, mean, maxv, minv = month_meta[i]
                    if image_blob is None:
                        logger.warning(f"No image for {month}, skipping.")
                        continue
                    image_base64 = base64.b64encode(image_blob).decode("utf-8")
                    results.append({
                        "month": month,
                        "ndvi_mean": mean,
                        "ndvi_max": maxv,
                        "ndvi_min": minv,
                        "image_base64": image_base64,
                    })
            return results

        result = asyncio.run(fetch_all_images())
        return JsonResponse(result, safe=False)

    except Exception as e:
        logger.error(f"Monthly NDVI summary error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ------------------ View: Carbon Credit Report ------------------

@csrf_exempt
def carbon_credit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry_data = data.get("geometry")
        start_date = data.get("start_date", "2025-02-23")
        end_date = data.get("end_date", "2025-03-23")

        if not geometry_data:
            return JsonResponse({'error': 'Missing geometry data'}, status=400)

        geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)

        # Step 1: NDVI stats → model input
        formatted_data = get_statistics_for_model_input(geometry_data, start_date, end_date)

        # Step 2: Predict biomass & CO2
        biomass_model = BiomassModelService(logger, model_path=MODEL_PATHS['biomass_model'], scaler_X_path=MODEL_PATHS['scaler_X'], scaler_y_path=MODEL_PATHS['scaler_y'])
        predicted_biomass = biomass_model.make_prediction(formatted_data)
        predicted_CO2 = convert_tree_biomass_array_to_CO2(predicted_biomass)

        # Step 3: Calculate area (GeoJSON assumed to be polygon)
        estimated_area_square = calculate_area_square(geometry_data['coordinates'][0])

        # Step 4: Generate PDF report
        buffer = generate_credit_report(start_date, end_date, estimated_area_square, geometry_data, predicted_CO2, formatted_data)
        filename = f"Carbon_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs(REPORT_PATH, exist_ok=True)
        file_path = os.path.join(REPORT_PATH, filename)
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        # Step 5: Write to database
        current_user = request.user
        farm_id = getattr(current_user, "currentFarm_id", None)
        farm = FarmInfo.objects.get(id=farm_id) if farm_id else None

        CarbonCredit.objects.create(
            farm=farm,
            start_date=start_date,
            end_date=end_date,
            file_path=f'report/{filename}',
            geolocation=geo_obj
        )

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        logger.error(f"Error generating carbon credit report: {e}")
        return JsonResponse({'error': str(e)}, status=500)

...

# ------------------ View: Carbon Credit Report ------------------

@csrf_exempt
def carbon_credit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry_data = data.get("geometry")
        start_date = data.get("start_date", "2025-02-23")
        end_date = data.get("end_date", "2025-03-23")

        if not geometry_data:
            return JsonResponse({'error': 'Missing geometry data'}, status=400)

        geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)
        formatted_data = get_statistics_for_model_input(geometry_data, start_date, end_date)

        biomass_model = BiomassModelService(logger, model_path=MODEL_PATHS['biomass_model'], scaler_X_path=MODEL_PATHS['scaler_X'], scaler_y_path=MODEL_PATHS['scaler_y'])
        predicted_biomass = biomass_model.make_prediction(formatted_data)
        predicted_CO2 = convert_tree_biomass_array_to_CO2(predicted_biomass)

        estimated_area_square = calculate_area_square(geometry_data['coordinates'][0])

        buffer = generate_credit_report(start_date, end_date, estimated_area_square, geometry_data, predicted_CO2, formatted_data)
        filename = f"Carbon_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs(REPORT_PATH, exist_ok=True)
        file_path = os.path.join(REPORT_PATH, filename)
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        current_user = request.user
        farm_id = getattr(current_user, "currentFarm_id", None)
        farm = FarmInfo.objects.get(id=farm_id) if farm_id else None

        CarbonCredit.objects.create(
            farm=farm,
            start_date=start_date,
            end_date=end_date,
            file_path=f'report/{filename}',
            geolocation=geo_obj
        )

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        logger.error(f"Error generating carbon credit report: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# ------------------ View: History for NDVI Region / Report / Carbon ------------------

@login_required
def region_history(request, farm_id):
    return _history_view(request, farm_id, NDVIRegion, 'Map/region_history.html', 'Map/region_history_fragment.html')

@login_required
def report_history(request, farm_id):
    return _history_view(request, farm_id, NDVIReport, 'Map/report_history.html', 'Map/report_history_fragment.html')

@login_required
def carbon_credit_history(request, farm_id):
    return _history_view(request, farm_id, CarbonCredit, 'Map/carbon_credit_history.html', 'Map/carbon_credit_history_fragment.html')


def _history_view(request, farm_id, model_class, full_template, fragment_template):
    farm = get_object_or_404(FarmInfo, id=farm_id, user_profiles=request.user)
    queryset = model_class.objects.filter(farm=farm).order_by('-created_at')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if start_date:
                queryset = queryset.filter(start_date__gte=parse_date(start_date))
            if end_date:
                queryset = queryset.filter(end_date__lte=parse_date(end_date))
        except Exception as e:
            logger.error(f"Error parsing request body: {e}")
            return JsonResponse({'error': 'Invalid request'}, status=400)

    context = {'farm': farm, 'reports': queryset}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, fragment_template, context)
    return render(request, full_template, context)


