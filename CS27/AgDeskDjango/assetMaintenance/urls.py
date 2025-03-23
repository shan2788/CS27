from django.urls import path
from . import views


urlpatterns = [
    path("asset/<str:assetCategory>/<int:assetID>/maintenance",
         views.viewMaintenance,          name="assetMaintenance"),
    path("asset/<str:assetCategory>/<int:assetID>/maintenance/<int:maintenanceID>/details",
         views.maintenanceDetails,       name="assetMaintenanceDetails"),
    path("asset/<str:assetCategory>/<int:assetID>/maintenance/<int:maintenanceID>/delete",
         views.deleteMaintenance,        name="deleteMaintenance"),
    path("asset/<str:assetCategory>/<int:assetID>/damage/<int:damageID>/delete",
         views.deleteDamage,             name="deleteDamage"),
    path("getMaintenanceDetails/<int:maintenance_id>/",
         views.get_maintenance_details,  name="get_maintenance_details"),
    path("asset/<str:assetCategory>/<int:assetID>/damage",
         views.viewDamage,               name="assetDamage"),
    path("asset/<str:assetCategory>/<int:assetID>/damage/<int:damageID>/details",
         views.damageDetails,            name="assetDamageDetails"),
    path("getDamageDetails/<int:damageLogID>/",
         views.retrieveDamageRecordByID, name="retrieveDamageRecordByID"),
]
