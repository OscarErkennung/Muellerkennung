from django.apps import AppConfig
from core.core_main import app_main
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self): 
        app_main()
        #startup code
