from django.conf import settings

if not settings.configured:
    settings.configure()


DATA_SOURCES_EXPLORE_APPS = getattr(settings, 'DATA_SOURCES_EXPLORE_APPS', [])
RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 10)
INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])
QUERIES_MAX_DAYS_IN_DATABASE = getattr(settings, 'QUERIES_MAX_DAYS_IN_DATABASE', 7)
