from django.urls import path

from . import views

urlpatterns = [
    path("checkout"                              , views.checkout    , name="checkout"    ),
    path("myCheckouts"                           , views.checkin     , name="myCheckouts" ),
    path("allCheckouts"                          , views.allCheckouts, name="allCheckouts"),
    path("<str:assetCategory>/<int:assetID>/logs", views.viewLogs    , name="assetLogs"   ),
    # path("current/farm"                          , views.currentLogs , name="checkin"     ),
    # path("logs/farm"                             , views.allLogs     , name="checkin"     )
]
