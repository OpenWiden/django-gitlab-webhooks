import pytest
from django.urls import resolve, reverse


@pytest.mark.parametrize(
    "namespace, url",
    [
        pytest.param("health_check", "/health_check/", id="health_check"),
        pytest.param("app_version", "/app_version/", id="app_version"),
    ],
)
def test_urls(namespace, url):
    assert reverse(namespace) == url
    assert resolve(url).view_name == namespace
