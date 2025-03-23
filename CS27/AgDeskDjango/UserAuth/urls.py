from django.urls import path
from . import views

urlpatterns = [
    # path("overview", views.adminOverview            ),
    path(""        , views.loginPage , name="login" ),
    path("logout/" , views.logoutUser, name="logout"),
    path("sign-up/", views.signup    , name="signup")
]