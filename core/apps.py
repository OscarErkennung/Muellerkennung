from django.apps import AppConfig
import os
from core.core_main import app_main
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self): 
        if os.environ.get('RUN_MAIN', None) == 'true':
            # This is the main process, not a worker
            print("Core app is ready, starting main application...")
            app_main()
        #startup code
