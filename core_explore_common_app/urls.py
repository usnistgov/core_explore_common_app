""" Url router for the Explore Common application
"""
from django.conf.urls import include
from django.urls import re_path

from core_explore_common_app.views.user import ajax as user_ajax

urlpatterns = [
    re_path(r"^rest/", include("core_explore_common_app.rest.urls")),
    re_path(
        r"^get_local_data_source",
        user_ajax.get_local_data_source,
        name="core_explore_common_get_local_data_source",
    ),
    re_path(
        r"^update-local-data-source",
        user_ajax.update_local_data_source,
        name="core_explore_common_update_local_data_source",
    ),
    re_path(
        r"^data-sources-html",
        user_ajax.get_data_sources_html,
        name="core_explore_common_data_sources_html",
    ),
    re_path(
        r"^data-source-results/(?P<query_id>\w+)/(?P<data_source_index>\w+)/(?P<page>\w+)$",
        user_ajax.get_data_source_results,
        name="core_explore_common_data_source_results",
    ),
    re_path(
        r"^data-source-results/(?P<query_id>\w+)/(?P<data_source_index>\w+)$",
        user_ajax.get_data_source_results,
        name="core_explore_common_data_source_results",
    ),
    re_path(
        r"^(?P<persistent_query_type>\w+)/(?P<persistent_query_id>\w+)",
        user_ajax.ContentPersistentQueryView.as_view(),
        name="core_explore_common_persistent_query_content",
    ),
]
