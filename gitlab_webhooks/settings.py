from django.conf import ImproperlyConfigured
from django.conf import settings as django_settings


def load_settings() -> None:
    try:
        settings = django_settings.GITLAB_WEBHOOKS
    except AttributeError:
        raise ImproperlyConfigured("GITLAB_WEBHOOKS settings is missing!")

    if not isinstance(settings, dict):
        raise ImproperlyConfigured("GITLAB_WEBHOOKS is not a dict!")

    # Your settings goes here ...
    # if "ALLOWED_EVENTS" not in settings:
    #     settings["ALLOWED_EVENTS"] = ["test"]
