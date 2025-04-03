from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.core.files.base import ContentFile
import json, requests, datetime, logging
from reportlab.pdfgen import canvas
from io import BytesIO
import joblib
import os
import numpy as np
import torch

from .models import NDVIRegion
from .sentinel_auth import get_sentinel_token, get_sentinel_instance_id
from  FarmAcc.models import FarmInfo

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
token = get_sentinel_token()

# Set up paths for model and encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CROP_MODEL_PATH = os.path.join(BASE_DIR, "rf_model.pkl")
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")
BIOMASS_MODEL_PATH = os.path.join(BASE_DIR, "biomass_model.pkl")

@login_required(login_url="login")
def map_view(request):
    sentinel_instance_id = get_sentinel_instance_id()
    return render(request, 'Map/map.html', {"sentinel_instance_id": sentinel_instance_id})


def get_ndvi_image_binary(geometry, start_date, end_date, evalscript):
    """
    img
    """

    payload = {
        "input": {
            "bounds": {
                "geometry": geometry
            },
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
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    logger.debug("Sending request to Sentinel Hub...")
    response = requests.post("https://services.sentinel-hub.com/api/v1/process", headers=headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Sentinel error {response.status_code}: {response.text}")


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

        image_data = get_ndvi_image_binary(geometry, start_date, end_date, evalscript_ndvi)
        # FIXME
        # # just for test
        # test_data = get_statistics_for_model_input(request)
        # print(test_data)
        return HttpResponse(image_data, content_type="image/png")

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
    

@login_required
def region_history(request, farm_id):
    """
    Show the history of NDVI regions for a farm of current user
    """
    # get the farm object
    farm = get_object_or_404(FarmInfo, id=farm_id, user_profiles=request.user)
    # get all regions for the farm
    regions = NDVIRegion.objects.filter(farm=farm).order_by('-created_at')
    return render(request, 'Map/region_history.html', {'farm': farm, 'regions': regions})

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
      if (sample.CLM > 0.5 || sample.dataMask === 0) {
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

    # Automatically generate statistics config for each band
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
        print(statistics_response)
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
                # FIXME: use mean instead of min
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

def make_crop_prediction(model, encoder, formatted_data):
    """
    Use the given model and encoder to predict the class of the plant.

    Args:
        model: The trained machine learning model (e.g., Random Forest).
        encoder: The label encoder used to encode class labels.
        formatted_data: A list of dictionaries, where each dictionary contains:
            - "from": Start of the time interval
            - "to": End of the time interval
            - "bands_mean": A dictionary of mean values for all bands
            - "ndvi_mean": The calculated NDVI mean value for the interval

    Returns:
        A string representing the predicted class of the plant.
    """
    try:
        # Extract the band values from the formatted data
        band_values = []
        for entry in formatted_data:
            bands_mean = entry["bands_mean"]
            # Ensure the order of bands matches the expected input format
            band_values.append([
                bands_mean.get("B01", 0),
                bands_mean.get("B02", 0),
                bands_mean.get("B03", 0),
                bands_mean.get("B04", 0),
                bands_mean.get("B05", 0),
                bands_mean.get("B06", 0),
                bands_mean.get("B07", 0),
                bands_mean.get("B08", 0),
                bands_mean.get("B8A", 0),
                bands_mean.get("B09", 0),
                bands_mean.get("B11", 0),
                bands_mean.get("B12", 0)
            ])

        # Convert to a NumPy array for model input
        band_values = np.array(band_values)

        # Make predictions using the model
        predictions = model.predict(band_values)

        # Ensure predictions are a 1D array
        predictions = np.array(predictions).flatten()

        # Decode the predicted labels using the encoder
        decoded_results = encoder.inverse_transform(predictions)

        return decoded_results

    except Exception as e:
        logger.error(f"Error in make_crop_prediction: {e}")
        return "Error in prediction"
    

def calculate_evi(bands_mean):
    """
    Calculate the Enhanced Vegetation Index (EVI) from band means.

    Args:
        bands_mean: A dictionary containing mean values for all bands.

    Returns:
        The calculated EVI value.
    """
    try:
        G = 2.5
        C1 = 6.0
        C2 = 7.5
        L = 1.0

        nir = bands_mean.get("B08", 0)  # Near-infrared band
        red = bands_mean.get("B04", 0)  # Red band
        blue = bands_mean.get("B02", 0)  # Blue band

        # Avoid division by zero
        denominator = (nir + C1 * red - C2 * blue + L)
        if denominator == 0:
            return 0

        evi = G * (nir - red) / denominator
        return evi

    except Exception as e:
        logger.error(f"Error calculating EVI: {e}")
        return 0
    

def make_biomass_prediction(model, formatted_data):
    """
    Predict biomass using the given model and formatted data.

    Args:
        model: The trained machine learning model for biomass prediction.
        formatted_data: A list of dictionaries, where each dictionary contains:
            - "from": Start of the time interval
            - "to": End of the time interval
            - "bands_mean": A dictionary of mean values for all bands
            - "ndvi_mean": The calculated NDVI mean value for the interval

    Returns:
        A list of predicted biomass values.
    """
    model.eval()  # Set the model to evaluation mode
    try:
        # Extract the band values and indices (NDVI, EVI) from the formatted data
        band_values = []
        for entry in formatted_data:
            bands_mean = entry["bands_mean"]
            ndvi_mean = entry.get("ndvi_mean", 0)  # NDVI mean value
            evi_mean = calculate_evi(bands_mean)  # Calculate EVI (see helper function below)

            # Ensure the order of inputs matches the expected input format
            band_values.append([
                ndvi_mean,  # NDVI
                evi_mean,   # EVI
                bands_mean.get("B01", 0),
                bands_mean.get("B02", 0),
                bands_mean.get("B03", 0),
                bands_mean.get("B04", 0),
                bands_mean.get("B05", 0),
                bands_mean.get("B06", 0),
                bands_mean.get("B07", 0),
                bands_mean.get("B08", 0),
                bands_mean.get("B8A", 0),
                bands_mean.get("B11", 0),
                bands_mean.get("B12", 0)
            ])

        # Convert to a NumPy array for model input
        band_values = np.array(band_values)
        band_values_tensor = torch.tensor(band_values, dtype=torch.float32)

        # Make predictions using the model
        with torch.no_grad():
            predictions = model(band_values_tensor)
        predictions = predictions.numpy()

        return predictions

    except Exception as e:
        logger.error(f"Error in make_biomass_prediction: {e}")
        return "Error in prediction"
    

def draw_wrapped_text(p, text, x, y, max_width, line_height=15):
    """
    Draw text with automatic line wrapping.

    Args:
        p: The canvas object.
        text: The text to draw.
        x: The x-coordinate for the text.
        y: The starting y-coordinate for the text.
        max_width: The maximum width of a line before wrapping.
        line_height: The height between lines.
    """
    from reportlab.pdfbase.pdfmetrics import stringWidth

    words = text.split(' ')
    line = ''
    for word in words:
        # Check if adding the next word exceeds the max width
        if stringWidth(line + word, p._fontname, p._fontsize) <= max_width:
            line += word + ' '
        else:
            # Draw the current line and start a new one
            p.drawString(x, y, line.strip())
            y -= line_height
            line = word + ' '
    # Draw the last line
    if line:
        p.drawString(x, y, line.strip())
    return y  # Return the final y-coordinate


@csrf_exempt
def generate_report(request):
    """
    Generate a report for the selected NDVI region
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        start_date = data.get('start_date', "2025-02-23")
        end_date = data.get('end_date', "2025-03-23")

        # Fetch NDVI statistics
        formatted_data = get_statistics_for_model_input(request)

        # get predicted crop and biomass
        crop_model = joblib.load(CROP_MODEL_PATH)
        encoder = joblib.load(CROP_ENCODER_PATH)
        predicted_crop = make_crop_prediction(crop_model, encoder, formatted_data)

        biomass_model = torch.load(BIOMASS_MODEL_PATH, weights_only=False)
        predicted_biomass = make_biomass_prediction(biomass_model, formatted_data)

        # Generate PDF report
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Title and metadata
        p.drawString(100, 800, "NDVI Report")
        p.drawString(100, 780, f"Start Date: {start_date}")
        p.drawString(100, 760, f"End Date: {end_date}")

        # Add predicted crop and biomass with wrapping
        y_position = 740
        y_position = draw_wrapped_text(p, f"Predicted Crop: {predicted_crop}", 100, y_position, max_width=400)
        y_position = draw_wrapped_text(p, f"Predicted Biomass: {predicted_biomass}", 100, y_position - 20, max_width=400)

        # Add NDVI mean and bands mean
        y_position -= 20
        for entry in formatted_data:
            y_position = draw_wrapped_text(p, f"Time Interval: {entry['from']} → {entry['to']}", 100, y_position, max_width=400)
            y_position -= 20
            y_position = draw_wrapped_text(p, f"NDVI Mean: {entry['ndvi_mean']:.4f}", 100, y_position, max_width=400)
            y_position -= 20
            p.drawString(100, y_position, "Bands Mean (x10000):")
            y_position -= 20

            for band, mean in entry["bands_mean"].items():
                y_position = draw_wrapped_text(p, f"{band}: {mean:.2f}", 120, y_position, max_width=400)
                y_position -= 20

            y_position -= 10
            if y_position < 100:
                p.showPage()
                y_position = 800

        # Save the PDF
        p.showPage()
        p.save()

        # Return PDF as response
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return JsonResponse({'error': str(e)}, status=500)