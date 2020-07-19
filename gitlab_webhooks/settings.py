from django.conf import ImproperlyConfigured
from django.conf import settings as django_settings

from .constants import Events

SETTINGS_KEY = "DJANGO_GITLAB_WEBHOOKS"


def load_settings() -> None:
    try:
        settings = getattr(django_settings, SETTINGS_KEY)
    except AttributeError:
        raise ImproperlyConfigured(
            "{settings_key} settings is missing!".format(settings_key=SETTINGS_KEY)
        )

    if not isinstance(settings, dict):
        raise ImproperlyConfigured(
            "{settings_key} is not a dict!".format(settings_key=SETTINGS_KEY)
        )

    if not settings.get("ALLOWED_EVENTS"):
        settings["ALLOWED_EVENTS"] = Events.values()
