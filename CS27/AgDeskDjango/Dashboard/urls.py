"""
Dashboard URLs.
"""

# Imports
from django.urls import path, include
from dashing.utils import router
from . import views


# Patterns
urlpatterns = [
    path("<int:farm_id>/home", views.mainDash       , name="home"           ),
    path("saveLayout"        , views.save_layout    , name="saveLayout"     ),
    path('getLayout/'        , views.get_layout     , name='getLayout'      ),
    path('deleteWidget'      , views.delete_widget  , name='deleteWidget'   ),
    path('update_my_tasks/'  , views.update_my_tasks, name='update_my_tasks'),
    path('dashboard/get_my_checkouts/', views.get_my_checkouts, name='get_my_checkouts'),
]
