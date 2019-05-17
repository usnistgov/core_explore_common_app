from django.conf import settings

from core_main_app.utils.query.constants import VISIBILITY_PUBLIC

if not settings.configured:
    settings.configure()


DATA_SOURCES_EXPLORE_APPS = getattr(settings, 'DATA_SOURCES_EXPLORE_APPS', [])
RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 10)
INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])
QUERIES_MAX_DAYS_IN_DATABASE = getattr(settings, 'QUERIES_MAX_DAYS_IN_DATABASE', 7)
EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY = getattr(settings,
                                                         'EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY',
                                                         True)
QUERY_VISIBILITY = getattr(settings, 'QUERY_VISIBILITY', VISIBILITY_PUBLIC)
