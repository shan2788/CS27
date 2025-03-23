from django.urls import path
from . import views



urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/ndvi/', views.ndvi_view, name='ndvi_view')
]
