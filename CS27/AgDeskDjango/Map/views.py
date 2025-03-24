from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json, requests
from .sentinel_auth import get_sentinel_token
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@login_required(login_url="login")
def map_view(request):
    return render(request, 'Map/map.html')


@csrf_exempt
def ndvi_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            geometry = data['geometry']
            start_date = data.get('start_date', "2025-02-23")
            end_date = data.get('end_date', "2025-03-23")

            sentinel_token = get_sentinel_token()

            evalscript_ndvi = """//VERSION=3
                function setup() {
                    return {
                        input: ["B04", "B08"],
                        output: { bands: 1, sampleType: "UINT8" }
                    };
                }
                function evaluatePixel(sample) {
                    let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
                    return [ndvi * 255];
                }"""

            url = "https://services.sentinel-hub.com/api/v1/process"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {sentinel_token}"
            }

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
                "evalscript": evalscript_ndvi
            }

            logger.debug(f"Sending request to {url} with payload: {json.dumps(payload, indent=2)} and headers: {headers}")

            response = requests.post(url, headers=headers, json=payload)

            logger.debug(f"Received response with status code {response.status_code} and content: {response.content}")

            if response.status_code == 200:
                return HttpResponse(response.content, content_type="image/png")
            else:
                return JsonResponse({
                    "error": "Sentinel Hub API error",
                    "status": response.status_code,
                    "detail": response.text
                })

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)
