import json

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.dispatch import Signal
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import constants, signals


@method_decorator(csrf_exempt, "dispatch")
class WebhookView(View):
    def get_secret(self) -> str:
        """
        Returns webhook's secret key.
        """
        secret = settings.DJANGO_GITLAB_WEBHOOKS.get("SECRET")
        if not secret:
            raise ImproperlyConfigured("SECRET key is not specified!")
        else:
            return secret

    @classmethod
    def event_is_allowed(cls, event: str) -> bool:
        if event in settings.DJANGO_GITLAB_WEBHOOKS["ALLOWED_EVENTS"]:
            return True
        else:
            return False

    @classmethod
    def get_signal(cls, event: str) -> Signal:
        formatted_event_name = event.lower().replace(" hook", "").replace(" ", "_")
        return getattr(signals, formatted_event_name)

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        # Validate webhook secret
        if request.META.get(constants.TOKEN_HEADER) != self.get_secret():
            return JsonResponse(
                {"detail": constants.INVALID_HTTP_X_GITLAB_TOKEN}, status=400,
            )

        # Check event header
        event = request.META.get(constants.EVENT_HEADER)
        if event is None:
            return JsonResponse(
                {"detail": constants.EVENT_HEADER_IS_MISSING}, status=400,
            )

        # Validate that event is allowed
        event_is_allowed = self.event_is_allowed(event)
        if event_is_allowed is False:
            return JsonResponse(
                {"detail": constants.EVENT_IS_NOT_ALLOWED.format(event=event)},
                status=400,
            )

        # Send signal on success event
        signal = self.get_signal(event)
        signal.send(__class__, payload=json.loads(request.body))

        return JsonResponse({"detail": "ok"})
