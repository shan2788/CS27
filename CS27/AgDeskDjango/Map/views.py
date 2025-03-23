from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, requests
@login_required(login_url="login")


def map_view(request):
    return render(request, 'Map/map.html')



@csrf_exempt
def ndvi_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            geometry = data['geometry']

            sentinel_token = "YOUR_SENTINEL_HUB_TOKEN"

            evalscript = """
            //VERSION=3
            function setup() {
              return {
                input: ["B04", "B08"],
                output: [{ id: "ndvi", bands: 1 }]
              };
            }

            function evaluatePixel(sample) {
              let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
              return { ndvi: [ndvi] };
            }
            """

            payload = {
                "input": {
                    "bounds": {
                        "geometry": geometry
                    },
                    "data": [{
                        "type": "sentinel-2-l2a"
                    }]
                },
                "aggregation": {
                    "timeRange": {
                        "from": "2023-03-01T00:00:00Z",
                        "to": "2023-03-31T23:59:59Z"
                    },
                    "aggregationInterval": {"value": 1, "unit": "DAYS"},
                    "resx": 10,
                    "resy": 10
                },
                "calculations": {
                    "default": {
                        "evalscript": evalscript
                    }
                }
            }

            response = requests.post(
                "https://services.sentinel-hub.com/api/v1/statistics",
                headers={
                    "Authorization": f"Bearer {sentinel_token}",
                    "Content-Type": "application/json"
                },
                json=payload
            )

            stats = response.json()['data'][0]['outputs']['ndvi']['bands'][0]['stats']
            return JsonResponse({'ndvi': stats['mean']})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)
