# ndvi_views.py (替代原来的 views.py 中 NDVI 相关部分)

import json, asyncio, os, datetime, base64
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.gis.geos import GEOSGeometry
from django.core.files.base import ContentFile
from .models import NDVIRegion
from FarmAcc.models import FarmInfo
from .services.ndvi_service import NDVIService
from django.conf import settings

ndvi_service = NDVIService()

@method_decorator(csrf_exempt, name='dispatch')
class NDVIImageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            geometry = data['geometry']
            start_date = data.get('start_date', "2025-02-23")
            end_date = data.get('end_date', "2025-03-23")

            image_data = asyncio.run(
                ndvi_service.get_ndvi_image(
                    geometry=geometry,
                    start_date=start_date,
                    end_date=end_date,
                    use_cache=False
                )
            )
            if image_data:
                return HttpResponse(image_data, content_type="image/png")
            return JsonResponse({'error': 'No image returned'}, status=500)

        except Exception as e:
            ndvi_service.logger.error("NDVI preview error: " + str(e))
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class NDVIImageSaveView(View):
    def post(self, request):
        try:
            user = request.user
            farm_id = user.currentFarm_id
            data = json.loads(request.body)
            geometry = data['geometry']
            start_date = data.get('start_date', "2025-02-23")
            end_date = data.get('end_date', "2025-03-23")

            region_id = asyncio.run(
                ndvi_service.fetch_and_save_ndvi(farm_id, geometry, start_date, end_date)
            )
            if region_id:
                return JsonResponse({'status': 'ok', 'id': region_id})
            return JsonResponse({'error': 'Failed to fetch or save image'}, status=500)

        except Exception as e:
            ndvi_service.logger.error("Save NDVI error: " + str(e))
            return JsonResponse({'error': str(e)}, status=400)
