from django.conf import settings

if not settings.configured:
    settings.configure()

DATA_SOURCES_EXPLORE_APPS = getattr(settings, 'DATA_SOURCES_EXPLORE_APPS', [])
