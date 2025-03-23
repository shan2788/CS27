from django.urls import path

from . import views
from assetMaintenance import views as maintenanceViews

urlpatterns = [
    path('<str:assetCategory>'                      , views.displayAssets, name='displayAssets'),
    path('add'                                      , views.createAsset  , name='addAsset'     ),
    path('<str:assetCategory>/<int:assetID>/details', views.viewAsset    , name='assetDetails' ),
    # path("/vehicles"                                , views.allVehicles  , name="allvehicles"  ),  
    # path("/sequipment"                              , views.allSEquipment, name="allsequipment"), 
    # path("/lequipment"                              , views.allLEquipment, name="alllequipment"),   
]
