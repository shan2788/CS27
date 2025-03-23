"""
URL configuration for AgDeskDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# Imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dashing.utils import router 


# Patterns
urlpatterns = [
    path("admin/"     , admin.site.urls                 ),
    path("userAdmin/" , include("UserAuth.urls"        )),
    path("farm/"      , include("FarmAcc.urls"         )),
    path(""           , include("UserAuth.urls"        )),
    path(""           , include("Dashboard.urls"       )),
    path("tasks/"     , include("Tasks.urls"           )),
    path("settings/"  , include("Settings.urls"        )),
    path("asset/"     , include("assetManagement.urls" )),
    path("operations/", include("assetOperation.urls"  )),
    path(""           , include("assetMaintenance.urls")),
    path("emergency/" , include("Emergency.urls"       )),
    path(""           , include("assetExpenses.urls"   )),
    path(""           , include(router.urls            ))
]


# For uploading files to the application
# https://www.geeksforgeeks.org/python-uploading-images-in-django/


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL               ,
        document_root=settings.MEDIA_ROOT
    )
