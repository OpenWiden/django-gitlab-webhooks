from django.urls import path

from . import views

urlpatterns = [
    path("health_check/", views.health_check_view, name="health_check"),
    path("app_version/", views.app_version_view, name="app_version"),
]
