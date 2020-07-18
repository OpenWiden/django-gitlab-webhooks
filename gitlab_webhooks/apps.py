from django.apps import AppConfig


class GitlabWebhooksConfig(AppConfig):
    name = "gitlab_webhooks"

    def ready(self):
        from . import settings

        settings.load_settings()
