from django.apps import AppConfig

class AjxSearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ajx_search"

    def ready(self):
        import ajx_search.signals
