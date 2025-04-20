from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
import json, requests, datetime, logging
import joblib
import os
import torch
import hashlib
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import datetime
import aiohttp
import asyncio

from io import BytesIO
import base64

from .models import NDVIRegion, NDVIReport
from .sentinel_auth import get_sentinel_token, get_sentinel_instance_id
from  FarmAcc.models import FarmInfo
from .predictions import make_crop_prediction, make_biomass_prediction, convert_tree_biomass_array_to_CO2
from .utils import generate_pdf_report, are_geometries_similar, calculate_area_square
from .test_pre import make_tree_recommendation, make_density_prediction, fake_carbon_series
from django.conf import settings
# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
token = get_sentinel_token()

# Set up paths for model and encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CROP_MODEL_PATH = os.path.join(BASE_DIR, "rf_model.pkl")
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")
BIOMASS_MODEL_PATH = os.path.join(BASE_DIR, "biomass_model.pkl")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_INDEX_PATH = os.path.join(CACHE_DIR, "cache_index.json")
SCALER_X_PATH = os.path.join(BASE_DIR, 'scaler_X.pkl')
SCALER_Y_PATH = os.path.join(BASE_DIR, 'scaler_y.pkl')

# Set up paths for report generation
REPORT_PATH = os.path.join(settings.MEDIA_ROOT, "report")

@login_required(login_url="login")
def map_view(request):
    sentinel_instance_id = get_sentinel_instance_id()
    return render(request, 'Map/map.html', {"sentinel_instance_id": sentinel_instance_id})


async def get_ndvi_image_binary(session, geometry, start_date, end_date, evalscript, use_cache=True):
    """
    异步请求 Sentinel Hub 获取 NDVI 图像（PNG 格式），支持缓存。
    参数:
        - session: aiohttp.ClientSession 实例
        - geometry: GeoJSON 格式的区域
        - start_date, end_date: 时间范围
        - evalscript: NDVI 渲染脚本
        - use_cache: 是否启用缓存
    返回:
        - 图像的二进制数据，或 None（请求失败）
    """

    cache_key = hashlib.md5(f"{geometry}_{start_date}_{end_date}".encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

    # ------------------ 缓存读取 ------------------
    if use_cache and os.path.exists(CACHE_INDEX_PATH):
        with open(CACHE_INDEX_PATH, "r") as f:
            cache_index = json.load(f)
        for cached_key, cached_data in cache_index.items():
            if are_geometries_similar(geometry, cached_data["geometry"], threshold=0.8):
                logger.info("Async cache hit based on geometry similarity.")
                cached_file = cached_data["cache_path"]
                if os.path.exists(cached_file):
                    with open(cached_file, "rb") as f:
                        return f.read()
    else:
        cache_index = {}

    # ------------------ 请求构建 ------------------
    payload = {
        "input": {
            "bounds": { "geometry": geometry },
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
                "format": { "type": "image/png" }
            }]
        },
        "evalscript": evalscript
    }

    headers = {
        "Authorization": f"Bearer {get_sentinel_token()}",
        "Content-Type": "application/json"
    }

    # ------------------ 异步请求 ------------------
    try:
        async with session.post("https://services.sentinel-hub.com/api/v1/process",
                                headers=headers, json=payload, timeout=30) as resp:
            if resp.status == 200:
                image_data = await resp.read()

                # 写入缓存
                if use_cache and image_data:
                    os.makedirs(CACHE_DIR, exist_ok=True)
                    with open(cache_path, "wb") as f:
                        f.write(image_data)
                    cache_index[cache_key] = {
                        "geometry": geometry,
                        "cache_path": cache_path
                    }
                    with open(CACHE_INDEX_PATH, "w") as f:
                        json.dump(cache_index, f)
                    logger.info("NDVI image saved to async cache.")
                return image_data
            else:
                logger.warning(f"Async Sentinel error {resp.status}: {await resp.text()}")
                return None
    except asyncio.TimeoutError:
        logger.error("Request to Sentinel timed out.")
        return None
    except Exception as e:
        logger.error(f"Async error in NDVI fetch: {e}")
        return None





@csrf_exempt
def ndvi_view(request):
    """
    only get pic, not save
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry = data['geometry']
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        evalscript_ndvi = """//VERSION=3
        function setup() {
            return {
                input: ["B04", "B08"],
                output: { bands: 4, sampleType: "UINT8" }
            };
        }
        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
            let r = 0, g = 0, b = 0, a = 255;

            if (ndvi < -0.2) {
                r = 0; g = 0; b = 0;
            } else if (ndvi < 0) {
                r = 165; g = 42; b = 42;
            } else if (ndvi < 0.2) {
                r = 255; g = 255; b = 0;
            } else if (ndvi < 0.4) {
                r = 0; g = 255; b = 0;
            } else {
                r = 0; g = 128; b = 0;
            }

            if (sample.B08 === 0 && sample.B04 === 0) {
                a = 0;
            }

            return [r, g, b, a];
        }"""

        async def fetch_ndvi():
            async with aiohttp.ClientSession() as session:
                return await get_ndvi_image_binary(
                    session=session,
                    geometry=geometry,
                    start_date=start_date,
                    end_date=end_date,
                    evalscript=evalscript_ndvi,
                    use_cache=False
                )

        image_data = asyncio.run(fetch_ndvi())

        if image_data:
            return HttpResponse(image_data, content_type="image/png")
        else:
            return JsonResponse({'error': 'No image returned'}, status=500)

    except Exception as e:
        logger.error("NDVI preview error: " + str(e))
        return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
def save_ndvi_result(request):
    """
    save
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)


    try:
        current_user = request.user
        farmID = current_user.currentFarm_id
        data = json.loads(request.body)
        geometry_data = data['geometry']
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")
        evalscript_ndvi = """//VERSION=3
        function setup() {
            return {
                input: ["B04", "B08"],
                output: { bands: 4, sampleType: "UINT8" }
            };
        }
        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
            let r = 0, g = 0, b = 0, a = 255;

            if (ndvi < -0.2) {
                r = 0; g = 0; b = 0;
            } else if (ndvi < 0) {
                r = 165; g = 42; b = 42;
            } else if (ndvi < 0.2) {
                r = 255; g = 255; b = 0;
            } else if (ndvi < 0.4) {
                r = 0; g = 255; b = 0;
            } else {
                r = 0; g = 128; b = 0;
            }

            if (sample.B08 === 0 && sample.B04 === 0) {
                a = 0;
            }

            return [r, g, b, a];
        }"""

        image_binary = get_ndvi_image_binary(geometry_data, start_date, end_date, evalscript_ndvi)
        geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)
        farm = FarmInfo.objects.get(id=farmID)
        region = NDVIRegion(farm=farm, geometry=geo_obj)
        filename = f"ndvi_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        region.image.save(filename, ContentFile(image_binary))
        region.save()

        return JsonResponse({'status': 'ok', 'id': region.id})

    except Exception as e:
        logger.error("Error saving NDVI region: " + str(e))
        return JsonResponse({'error': str(e)}, status=400)


def get_statistics_data(request):
    token = get_sentinel_token()
    data = json.loads(request.body)
    geometry = data["geometry"]
    start_date = data.get("start_date", "2025-02-28")
    end_date = data.get("end_date", "2025-03-28")

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
            "bounds": {
                "geometry": geometry
            },
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
        "calculations": {
            "default": {
                "statistics": stats
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://services.sentinel-hub.com/api/v1/statistics", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Statistics error {response.status_code}: {response.text}")


def get_statistics_for_model_input(request):
    """
    Extract useful data from the statistics response and format it for model input.
    Outputs:
        A list of dictionaries, where each dictionary contains:
        - "from": Start of the time interval
        - "to": End of the time interval
        - "bands_mean": A dictionary of mean values for all bands
        - "ndvi_mean": The calculated NDVI mean value for the interval
    """
    try:
        # get statistics data from the request
        statistics_response = get_statistics_data(request)
        data_list = statistics_response.get("data", [])

        # Initialize results list
        results = []

        for entry in data_list:
            interval = entry.get("interval", {})
            outputs = entry.get("outputs", {})

            # extract band statistics
            bands_mean = {}
            for band_name, band_data in outputs.items():
                band_stats = band_data.get("bands", {}).get("B0", {}).get("stats", {})
                mean_value = band_stats.get("mean", None)
                if mean_value is not None:
                    bands_mean[band_name] = mean_value * 10000  # 将平均值乘以 10000
                else:
                    bands_mean[band_name] = None

            # calculate NDVI mean
            b08_mean = bands_mean.get("B08", None)  # NIR
            b04_mean = bands_mean.get("B04", None)  # Red
            ndvi_mean = None
            if b08_mean is not None and b04_mean is not None and (b08_mean + b04_mean) != 0:
                ndvi_mean = (b08_mean - b04_mean) / (b08_mean + b04_mean)

            # add to results
            results.append({
                "from": interval.get("from"),
                "to": interval.get("to"),
                "bands_mean": bands_mean,
                "ndvi_mean": ndvi_mean
            })

        # return results
        return results

    except Exception as e:
        logger.error(f"Error processing statistics for model input: {e}")
        return []




@csrf_exempt
def generate_report(request):
    """
    Generate a report for the selected NDVI region and save it.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")
        geometry_data = data.get("geometry")

        if not geometry_data:
            return JsonResponse({'error': 'Missing geometry data'}, status=400)

        # Convert geometry to GEOS object
        geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)

        # Get statistics and run predictions
        formatted_data = get_statistics_for_model_input(request)

        crop_model = joblib.load(CROP_MODEL_PATH)
        encoder = joblib.load(CROP_ENCODER_PATH)
        predicted_crop = make_crop_prediction(crop_model, encoder, formatted_data, logger)

        biomass_model = torch.load(BIOMASS_MODEL_PATH, weights_only=False)
        scaler_X = joblib.load(SCALER_X_PATH)
        scaler_y = joblib.load(SCALER_Y_PATH)
        predicted_biomass = make_biomass_prediction(biomass_model, scaler_X, scaler_y, formatted_data, logger)
        predicted_CO2 = convert_tree_biomass_array_to_CO2(predicted_biomass)
        # estimated_area_square = float(calculate_area_square(geometry_data))


        # Generate PDF report
        buffer = generate_pdf_report(start_date, end_date, predicted_crop, predicted_biomass, predicted_CO2, formatted_data)

        # Save PDF to filesystem
        filename = f"NDVI_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        save_dir = REPORT_PATH
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)

        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        # Get current user's farm
        current_user = request.user
        farm_id = getattr(current_user, "currentFarm_id", None)
        farm = FarmInfo.objects.get(id=farm_id) if farm_id else None

        # Save record to database
        NDVIReport.objects.create(
            farm=farm,
            start_date=start_date,
            end_date=end_date,
            file_path=f'report/{filename}',
            geolocation=geo_obj
        )

        # Return the PDF response
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def tree_recommendation_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        geometry = data.get('geometry')
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        formatted_data = get_statistics_for_model_input(request)  #model——ndvi

        # 预测结果（还没有）
        #species = make_tree_recommendation(formatted_data)
        #density = make_density_prediction(formatted_data)
        #carbon = 2.3 

        species = make_tree_recommendation(formatted_data)
        density = make_density_prediction(formatted_data)
        carbon_list = fake_carbon_series(density)
        years = ["2025", "2026", "2027", "2028", "2029"]

        plt.figure()
        plt.plot(years, carbon_list, marker='o')
        plt.title("predicted change")
        plt.xlabel("years")
        plt.ylabel("carbon emission(ton/year)")
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        chart_base64 = base64.b64encode(image_png).decode("utf-8")

        html = render_to_string("Map/tree_result_fragment.html", {
            "species": species,
            "density": density,
            "carbon": chart_base64,
        })

        return HttpResponse(html)


@login_required
def region_history(request, farm_id):
    """
    Show the history of NDVI regions for a farm of current user
    """
    farm = get_object_or_404(FarmInfo, id=farm_id, user_profiles=request.user)
    regions = NDVIRegion.objects.filter(farm=farm).order_by('-created_at')

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'Map/region_history_fragment.html', {'farm': farm, 'regions': regions})

    # Fallback for non-AJAX requests
    return render(request, 'Map/region_history.html', {'farm': farm, 'regions': regions})


@login_required
def report_history(request, farm_id):
    """
    Show the history of NDVI reports for a farm of the current user, filtered by date range.
    """
    farm = get_object_or_404(FarmInfo, id=farm_id, user_profiles=request.user)
    reports = NDVIReport.objects.filter(farm=farm).order_by('-created_at')

    if request.method == 'POST':
        # Get start_date and end_date from request parameters
        try:
            data = json.loads(request.body)
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            logger.debug(f"Start date: {start_date}, End date: {end_date}")

            if start_date:
                start_date = parse_date(start_date)
                reports = reports.filter(start_date__gte=start_date)

            if end_date:
                end_date = parse_date(end_date)
                reports = reports.filter(end_date__lte=end_date)

        except Exception as e:
            logger.error(f"Error parsing request body: {e}")
            return JsonResponse({'error': 'Invalid request'}, status=400)

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'Map/report_history_fragment.html', {'farm': farm, 'reports': reports})

    # Fallback for non-AJAX requests
    return render(request, 'Map/report_history.html', {'farm': farm, 'reports': reports})

@csrf_exempt
def ndvi_monthly_summary(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        geometry = data['geometry']
        start_date = data['start_date']
        end_date = data['end_date']

        weekly_stats = get_statistics_for_model_input(request)
        if not weekly_stats:
            return JsonResponse({'error': 'No weekly data found'}, status=404)

        # ------------------ 每月聚合 ------------------
        monthly_data = defaultdict(list)
        for entry in weekly_stats:
            date_obj = datetime.datetime.fromisoformat(entry["from"][:10])
            month_key = date_obj.strftime("%Y-%m")
            monthly_data[month_key].append(entry)

        # ------------------ 准备任务 ------------------
        month_meta = []
        month_tasks = []

        evalscript_ndvi = """//VERSION=3
        function setup() {
            return { input: ["B04", "B08"], output: { bands: 4, sampleType: "UINT8" }};
        }
        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
            let r = 0, g = 0, b = 0, a = 255;
            if (ndvi < -0.2) { r=0;g=0;b=0; }
            else if (ndvi < 0) { r=165;g=42;b=42; }
            else if (ndvi < 0.2) { r=255;g=255;b=0; }
            else if (ndvi < 0.4) { r=0;g=255;b=0; }
            else { r=0;g=128;b=0; }
            if (sample.B08 === 0 && sample.B04 === 0) a = 0;
            return [r, g, b, a];
        }"""

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
            month_tasks.append((geometry, mid_from, mid_to, evalscript_ndvi))


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
