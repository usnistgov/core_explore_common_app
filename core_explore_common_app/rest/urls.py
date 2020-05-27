"""Url router for the REST API
"""

from django.urls import re_path

from core_explore_common_app.rest.query import views as query_views
from core_explore_common_app.rest.result import views as result_views

urlpatterns = [
    re_path(
        r"^local-query",
        query_views.ExecuteLocalQueryView.as_view(),
        name="core_explore_common_local_query",
    ),
    re_path(
        r"^result",
        result_views.get_result_from_data_id,
        name="core_explore_common_app_get_result_from_data_id",
    ),
]
