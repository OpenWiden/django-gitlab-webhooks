from django.urls import path

from .views import WebhookView

urlpatterns = [
    path("receive/", WebhookView.as_view(), name="receive"),
]
