import json

import pytest
from django.test import RequestFactory
from gitlab_webhooks import __version__, views


def test_health_check_view(rf: RequestFactory):
    request = rf.get("/fake-url/")
    response = views.HealthCheckView().get(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"detail": "ok"}


def test_app_version_view(rf: RequestFactory):
    request = rf.get("/fake-url/")
    response = views.AppVersionView().get(request)

    assert response.status_code == 200
    assert json.loads(response.content) == {"detail": __version__}
