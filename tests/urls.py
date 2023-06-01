""" Url router for the core explore common test application
"""
from django.urls import re_path

from core_explore_common_app.rest.result import views as result_views
from core_main_app.rest.data import views as data_views
from core_main_app.views.common import (
    views as common_views,
)

urlpatterns = [
    re_path(
        r"^data",
        common_views.ViewData.as_view(),
        name="core_main_app_data_detail",
    ),
    re_path(
        r"^data/permissions/$",
        data_views.DataPermissions.as_view(),
        name="core_main_app_rest_data_permissions",
    ),
    re_path(
        r"^result",
        result_views.get_result_from_data_id,
        name="core_explore_common_app_get_result_from_data_id",
    ),
    re_path(
        r"^blob",
        common_views.ViewBlob.as_view(),
        name="core_main_app_blob_detail",
    ),
]
