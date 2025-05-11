from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

import os, json, logging

from .models import NDVIRegion, NDVIReport, CarbonCredit
from FarmAcc.models import FarmInfo

from .services.history_service import HistoryService
from .services.sentinel_service import SentinelService
from .services.prediction_service import CropModelService, BiomassModelService
from .services.pdf_service import PDFService
from .services.geo_service import GeoService
from .test_pre import make_tree_recommendation, make_density_prediction, fake_carbon_series
from .services.ndvi_service import NDVIService
from .services.statistics_service import StatisticsService
from .services.report_service import ReportGenerator
from .services.tree_recommendation_service import TreeRecommendationService
from .utils.decorators import handle_view_errors

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
MODEL_PATHS = settings.MODEL_PATHS
REPORT_PATH = settings.REPORT_PATH
NDVI_EVALSCRIPT = settings.NDVI_EVALSCRIPT
SENTINEL_SERVICE = SentinelService()

def extract_geometry_dates(request):
    data = json.loads(request.body)
    geometry = data.get("geometry")
    start_date = data.get("start_date", "2025-02-23")
    end_date = data.get("end_date", "2025-03-23")
    return geometry, start_date, end_date

@login_required(login_url="login")
def map_view(request):
    return render(request, 'Map/map.html', {"sentinel_instance_id": SENTINEL_SERVICE.get_instance_id()})

@csrf_exempt
@require_POST
@handle_view_errors(logger)
def generate_report(request):
    geometry, start_date, end_date = extract_geometry_dates(request)
    if not geometry:
        return JsonResponse({'error': 'Missing geometry data'}, status=400)
    generator = ReportGenerator(MODEL_PATHS, REPORT_PATH, logger)
    pdf_buffer, _ = generator.generate(geometry, start_date, end_date, request.user)
    return HttpResponse(pdf_buffer, content_type='application/pdf')

@csrf_exempt
@require_POST
@handle_view_errors(logger)
def tree_recommendation_view(request):
    geometry, start_date, end_date = extract_geometry_dates(request)
    service = TreeRecommendationService()
    html = service.generate(geometry, start_date, end_date)
    return HttpResponse(html)

@csrf_exempt
@require_POST
@handle_view_errors(logger)
def ndvi_monthly_summary(request):
    geometry, start_date, end_date = extract_geometry_dates(request)
    result = NDVIService.generate_monthly_summary(
        geometry=geometry,
        start_date=start_date,
        end_date=end_date,
        eval_script=NDVI_EVALSCRIPT,
        logger=logger
    )
    return JsonResponse(result, safe=False)

@csrf_exempt
@require_POST
@handle_view_errors(logger)
def carbon_credit(request):
    geometry_data, start_date, end_date = extract_geometry_dates(request)
    if not geometry_data:
        return JsonResponse({'error': 'Missing geometry data'}, status=400)
    service = ReportGenerator(MODEL_PATHS, REPORT_PATH, logger)
    pdf_buffer = service.generate_carbon_report(geometry_data, start_date, end_date, request.user)
    return HttpResponse(pdf_buffer, content_type='application/pdf')

@login_required
def region_history(request, farm_id):
    return _history_view(request, farm_id, NDVIRegion, 'Map/region_history.html', 'Map/region_history_fragment.html')

@login_required
def report_history(request, farm_id):
    return _history_view(request, farm_id, NDVIReport, 'Map/report_history.html', 'Map/report_history_fragment.html')

@login_required
def carbon_credit_history(request, farm_id):
    return _history_view(request, farm_id, CarbonCredit, 'Map/carbon_credit_history.html', 'Map/carbon_credit_history_fragment.html')

@handle_view_errors(logger)
def _history_view(request, farm_id, model_class, full_template, fragment_template):
    farm = get_object_or_404(FarmInfo, id=farm_id, user_profiles=request.user)
    queryset = HistoryService.get_filtered_queryset(request, model_class, farm, logger)
    context = {'farm': farm, 'reports': queryset}
    template = fragment_template if request.headers.get('x-requested-with') == 'XMLHttpRequest' else full_template
    return render(request, template, context)
