from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/ndvi/', views.ndvi_view, name='ndvi_view'),
    path('api/save-ndvi/', views.save_ndvi_result, name='save_ndvi_result'),
    path('api/generate-report/', views.generate_report, name='generate_report'),
    path('recommend-tree/', views.tree_recommendation_view, name='tree-recommendation'),
    path('api/region-history/<int:farm_id>/', views.region_history, name='region_history'),
    path('api/report-history/<int:farm_id>/', views.report_history, name='report_history'),
    path('api/carbon-credit/', views.carbon_credit, name='carbon_credit'),
    path('api/carbon-credit-history/<int:farm_id>/', views.carbon_credit_history, name='carbon_credit_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

