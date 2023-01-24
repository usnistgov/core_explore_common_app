"""Url router for the REST API
"""

from django.urls import re_path

from core_explore_common_app.rest.result import views as result_views

urlpatterns = [
    re_path(
        r"^result",
        result_views.get_result_from_data_id,
        name="core_explore_common_app_get_result_from_data_id",
    ),
]
