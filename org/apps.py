from django.apps import AppConfig


class OrgConfig(AppConfig):
    name = 'org'
    
    def ready(self):
        from . import signals