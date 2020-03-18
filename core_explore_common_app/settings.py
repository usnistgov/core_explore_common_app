from django.conf import settings

from core_main_app.utils.query.constants import VISIBILITY_PUBLIC

if not settings.configured:
    settings.configure()

CUSTOM_NAME = getattr(settings, 'CUSTOM_NAME', 'Local')
""" :py:class:`str`: Name of the local instance
"""

DATA_SOURCES_EXPLORE_APPS = getattr(settings, 'DATA_SOURCES_EXPLORE_APPS', [])
RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 10)
INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])
QUERIES_MAX_DAYS_IN_DATABASE = getattr(settings, 'QUERIES_MAX_DAYS_IN_DATABASE', 7)
EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY = getattr(settings,
                                                         'EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY',
                                                         True)
QUERY_VISIBILITY = getattr(settings, 'QUERY_VISIBILITY', VISIBILITY_PUBLIC)

"""The default sorting fields displayed on the GUI, Data model field Array"""
DATA_DISPLAYED_SORTING_FIELDS = getattr(settings, 'DATA_DISPLAYED_SORTING_FIELDS', [{'field': 'title', 'display': 'Title'},
                                                                                 {'field': 'last_modification_date', 'display': 'Last modification date'},
                                                                                 {'field': 'template', 'display': 'Template'}])

"""Set the toggle default value in the records list"""
DEFAULT_DATE_TOGGLE_VALUE = getattr(settings, 'DEFAULT_DATE_TOGGLE_VALUE', False)

"""Display the edit button on the result page"""
DISPLAY_EDIT_BUTTON = getattr(settings, 'DISPLAY_EDIT_BUTTON', False)

"""Result sorting graphical display type ('multi' / 'single')"""
SORTING_DISPLAY_TYPE = getattr(settings, 'SORTING_DISPLAY_TYPE', 'single')
