import pytest
from django.core.exceptions import ImproperlyConfigured
from gitlab_webhooks import settings as app_settings


def test_load_settings_success():
    app_settings.load_settings()


def test_missed_settings(settings):
    del settings.DJANGO_GITLAB_WEBHOOKS
    with pytest.raises(ImproperlyConfigured):
        app_settings.load_settings()


def test_settings_is_not_a_dict(settings):
    settings.DJANGO_GITLAB_WEBHOOKS = list()
    with pytest.raises(ImproperlyConfigured):
        app_settings.load_settings()
