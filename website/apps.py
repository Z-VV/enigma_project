from django.apps import AppConfig

class WebsiteConfig(AppConfig):
    name = 'website'

    def ready(self):
        # import signal handlers
        import website.signals



