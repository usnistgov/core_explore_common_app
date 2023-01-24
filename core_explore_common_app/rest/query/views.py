""" REST views for the query API
"""
import json
import logging

import pytz
from django.conf import settings as conf_settings
from django.urls import reverse

from core_explore_common_app.components.result.models import Result
from core_explore_common_app.utils.linked_records import pid as pid_utils
from core_explore_common_app.utils.result import result as result_utils
from core_main_app.commons.constants import DATA_JSON_FIELD
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.data import api as data_api
from core_main_app.rest.data.abstract_views import (
    AbstractExecuteLocalQueryView,
)
from core_main_app.settings import DATA_SORTING_FIELDS, RESULTS_PER_PAGE
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_main_app.utils.pagination.mongoengine_paginator.paginator import (
    MongoenginePaginator,
)
from core_main_app.utils.query.constants import VISIBILITY_OPTION
from core_main_app.utils.query.mongo.query_builder import QueryBuilder

logger = logging.getLogger(__name__)


def execute_local_query(query_data, page, request):
    """Execute query on local database

    Args:
        query_data:
        page:
        request:

    Returns:

    """
    # get query and templates
    query = query_data.get("query", None)

    if query is None:
        raise ApiError("Query should be passed in parameter.")

    templates = query_data.get("templates", [])
    if type(templates) is str:
        templates = json.loads(templates)
    options = query_data.get("options", {})
    if type(options) is str:
        options = json.loads(options)
    order_by_field = query_data.get("order_by_field", "")
    order_by_field = (
        order_by_field.split(",") if order_by_field else DATA_SORTING_FIELDS
    )

    # build query builder
    query_builder = QueryBuilder(query, DATA_JSON_FIELD)

    # update the criteria with templates information
    if templates is not None and len(templates) > 0:
        list_template_ids = [
            AbstractExecuteLocalQueryView.parse_id(template["id"])
            for template in templates
        ]
        query_builder.add_list_criteria("template", list_template_ids)
    # update the criteria with visibility information
    if options is not None and VISIBILITY_OPTION in options:
        query_builder.add_visibility_criteria(options[VISIBILITY_OPTION])

    # get raw query
    raw_query = query_builder.get_raw_query()
    # execute query
    data_list = data_api.execute_json_query(
        raw_query, request.user, order_by_field
    )
    # paginate results
    if conf_settings.MONGODB_INDEXING:
        paginator = MongoenginePaginator(data_list, RESULTS_PER_PAGE)
        page = paginator.get_page(page)
    else:
        paginator = ResultsPaginator()
        page = paginator.get_results(data_list, page, RESULTS_PER_PAGE)
    return page


def format_local_results(results, request):
    """Format local results for explore app

    Args:
        results:
        request:

    Returns:

    """
    # Get detail view base url (to be completed with data id)
    detail_url_base = reverse("core_main_app_data_detail")
    url_access_data = reverse(
        "core_explore_common_app_get_result_from_data_id"
    )
    url_permission_data = reverse("core_main_app_rest_data_permissions")

    # Template info
    template_info = dict()
    # Init data list
    data_list = []

    for data in results.object_list:
        # get data's template
        template_id = data.template_id
        # get and store data's template information
        if template_id not in template_info:
            template_info[template_id] = result_utils.get_template_info(
                data.template
            )

        detail_url = f"{detail_url_base}?id={str(data.id)}"

        # Use the PID link if the app is installed, and a PID is defined for the document
        if pid_utils.auto_set_pid_enabled(
            installed_apps=conf_settings.INSTALLED_APPS
        ):
            pid_url = pid_utils.get_pid_url(data, request)
            # Ensure the PID is set
            detail_url = pid_url if pid_url else detail_url

        data_list.append(
            Result(
                title=data.title,
                xml_content=data.xml_content,
                template_info=template_info[template_id],
                permission_url=f'{url_permission_data}?ids=%5B"{str(data.id)}"%5D',
                detail_url=detail_url,
                access_data_url=f"{url_access_data}?id={data.id}",
                last_modification_date=data.last_modification_date.replace(
                    tzinfo=pytz.UTC
                ),
            )
        )
    return data_list
