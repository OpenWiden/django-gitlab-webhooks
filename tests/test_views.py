import json

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory
from gitlab_webhooks import constants
from gitlab_webhooks.views import WebhookView


class TestWebhookView:
    @pytest.mark.parametrize("event", constants.Events.values())
    def test_success(self, rf: RequestFactory, settings, event: str):
        settings.DJANGO_GITLAB_WEBHOOKS = {
            "SECRET": "fake_token",
            "ALLOWED_EVENTS": [event],
        }
        headers = {
            constants.TOKEN_HEADER: "fake_token",
            constants.EVENT_HEADER: event,
        }
        request = rf.post("/fake-url/", **headers)
        request._body = '{"test": "ok"}'.encode()
        response = WebhookView().post(request)

        assert response.status_code == 200
        assert json.loads(response.content) == {"detail": "ok"}

    def test_get_secret(self, settings):
        settings.DJANGO_GITLAB_WEBHOOKS = {}

        with pytest.raises(ImproperlyConfigured):
            WebhookView().get_secret()

    def test_invalid_token(self, rf: RequestFactory, settings):
        settings.DJANGO_GITLAB_WEBHOOKS = {"SECRET": "fake_token"}
        headers = {constants.TOKEN_HEADER: "invalid"}
        request = rf.post("/fake-url/", **headers)
        response = WebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.INVALID_HTTP_X_GITLAB_TOKEN
        }

    def test_event_header_is_missing(self, rf: RequestFactory, settings):
        settings.DJANGO_GITLAB_WEBHOOKS = {"SECRET": "fake_token"}
        headers = {constants.TOKEN_HEADER: "fake_token"}
        request = rf.post("/fake-url/", **headers)
        response = WebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.EVENT_HEADER_IS_MISSING
        }

    def test_event_is_not_allowed(self, rf: RequestFactory, settings):
        settings.DJANGO_GITLAB_WEBHOOKS = {"SECRET": "fake_token", "ALLOWED_EVENTS": []}
        headers = {constants.TOKEN_HEADER: "fake_token", constants.EVENT_HEADER: "test"}
        request = rf.post("/fake-url/", **headers)
        response = WebhookView().post(request)

        assert response.status_code == 400
        assert json.loads(response.content.decode()) == {
            "detail": constants.EVENT_IS_NOT_ALLOWED.format(event="test")
        }
