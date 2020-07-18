from django import views
from django.http import HttpRequest, JsonResponse
from gitlab_webhooks import __version__


class HealthCheckView(views.View):
    def get(self, request: HttpRequest):
        return JsonResponse({"detail": "ok"})


health_check_view = HealthCheckView.as_view()


class AppVersionView(views.View):
    def get(self, request: HttpRequest):
        return JsonResponse({"detail": __version__})


app_version_view = AppVersionView.as_view()
