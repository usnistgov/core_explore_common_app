"""AJAX Explore common user views
"""
import json
import math
from abc import ABCMeta, abstractmethod
from os.path import join

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render as django_render
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views import View

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.pagination.rest_framework_paginator.rest_framework_paginator import (
    get_page_number,
)
from core_main_app.views.common.views import CommonView

from core_explore_common_app import settings
from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.components.abstract_persistent_query import (
    api as abstract_persistent_query_api,
)
from core_explore_common_app.components.abstract_persistent_query.models import (
    AbstractPersistentQuery,
)
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_explore_common_app.utils.query.query import (
    send as send_query,
    add_local_data_source,
    get_local_query_absolute_url,
)


def get_local_data_source(request):
    """Ajax method to get the local data source

    Args:
        request:

    Returns:

    """
    try:
        id_query = request.GET.get("query_id", None)

        if id_query is not None:
            # Get query from id
            query = query_api.get_by_id(id_query, request.user)

            context_params = {
                "enabled": True,
                "selected": False,
            }
            if len(settings.DATA_SOURCES_EXPLORE_APPS) == 0:
                add_local_data_source(request, query)
                context_params["enabled"] = False

            # check query to see if local data source was selected
            local_query_url = get_local_query_absolute_url(request)
            for data_source in query.data_sources:
                if (
                    data_source["name"] == LOCAL_QUERY_NAME
                    and data_source["url_query"] == local_query_url
                ):
                    context_params["selected"] = True

            context = {}
            context.update(request)
            context.update(context_params)
            return django_render(
                request,
                "core_explore_common_app/user/selector/local_content.html",
                context=context,
            )

        return HttpResponseBadRequest("Expected query_id parameter is missing.")

    except DoesNotExist:
        return HttpResponseBadRequest("The query does not exist.")
    except Exception:
        return HttpResponseBadRequest(
            "An unexpected error occurred while getting local data source selector."
        )


def update_local_data_source(request):
    """Ajax method to update query with local data source

    Args:
        request:

    Returns:

    """
    try:
        query_id = request.GET["query_id"]
        selected = json.loads(request.GET["selected"])

        # Get query from id
        query = query_api.get_by_id(query_id, request.user)

        if selected:
            # Local data source is selected, add it to the query as a data source
            add_local_data_source(request, query)
        else:
            # Local data source is not selected, remove it from the query
            local_query_url = get_local_query_absolute_url(request)
            data_source = query_api.get_data_source_by_name_and_url_query(
                query, LOCAL_QUERY_NAME, local_query_url, request.user
            )
            query_api.remove_data_source(query, data_source, request.user)

        return HttpResponse()

    except DoesNotExist:
        return HttpResponseBadRequest("The query does not exist.")
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))


def get_data_sources_html(request):
    """Gets data sources html for results

    Args:
        request:

    Returns:

    """
    try:
        # get query id
        query_id = request.POST["query_id"]

        # get query results
        query = query_api.get_by_id(query_id, request.user)

        # Check if 'core_linked_records_app' is installed and activated
        is_linked_records_installed = False
        if "core_linked_records_app" in settings.INSTALLED_APPS:
            from core_linked_records_app.components.pid_settings import (
                api as pid_settings_api,
            )

            is_linked_records_installed = pid_settings_api.get().auto_set_pid

        # set query in context
        context = {
            "linked_records_app": is_linked_records_installed,
            "exporter_app": "core_exporters_app" in settings.INSTALLED_APPS,
            "sorting_display_type": settings.SORTING_DISPLAY_TYPE,
            "data_displayed_sorting_fields": settings.DATA_DISPLAYED_SORTING_FIELDS,
            "default_date_toggle_value": settings.DEFAULT_DATE_TOGGLE_VALUE,
        }
        context.update({"query": query})

        # render html results
        html_template = loader.get_template(
            join(
                "core_explore_common_app",
                "user",
                "results",
                "data_sources_results.html",
            )
        )
        html_results_holders = html_template.render(context)

        response_dict = {"results": html_results_holders}
        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    except DoesNotExist:
        return HttpResponseBadRequest("The query does not exist.")
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))


def get_data_source_results(request, query_id, data_source_index, page=1):
    """Gets results from a data source

    Args:
        request:
        query_id:
        data_source_index:
        page:

    Returns:

    """
    try:
        # get query
        query = query_api.get_by_id(query_id, request.user)

        # send query, and get results from data source
        results = send_query(request, query, int(data_source_index), page)

        # get pagination information
        previous_page_number = get_page_number(results["previous"])
        next_page_number = get_page_number(results["next"])
        results_count = results["count"]
        page_count = int(math.ceil(float(results_count) / settings.RESULTS_PER_PAGE))

        # pagination has other pages?
        has_other_pages = results_count > settings.RESULTS_PER_PAGE

        # pagination has previous?
        has_previous = previous_page_number is not None

        # pagination has next?
        has_next = next_page_number is not None and next_page_number <= page_count

        # set results in context
        context_data = {
            "results": results["results"],
            "query_id": query_id,
            "data_source_index": data_source_index,
            "pagination": {
                "number": int(page),
                "paginator": {"num_pages": page_count},
                "has_other_pages": has_other_pages,
                "previous_page_number": previous_page_number,
                "next_page_number": next_page_number,
                "has_previous": has_previous,
                "has_next": has_next,
            },
            "blobs_preview": "core_file_preview_app" in settings.INSTALLED_APPS,
            "display_edit_button": settings.DISPLAY_EDIT_BUTTON,
            "exporter_app": "core_exporters_app" in settings.INSTALLED_APPS,
        }

        # create context
        context = {}
        context.update(request)
        context.update(context_data)

        # generate html with context
        html_template = loader.get_template(
            join(
                "core_explore_common_app", "user", "results", "data_source_results.html"
            )
        )
        # render html
        results_html = html_template.render(context)
        # set response with html results
        response_dict = {"results": results_html, "nb_results": results["count"]}
        return HttpResponse(json.dumps(response_dict), content_type="application/json")

    except DoesNotExist:
        return HttpResponseBadRequest("The query does not exist.")
    except ExploreRequestError as ex:
        return HttpResponseBadRequest(
            "An error occurred while sending the query: " + escape(str(ex)),
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            "An unexpected error occurred: " + escape(str(exception)),
        )


class CreatePersistentQueryUrlView(View, metaclass=ABCMeta):
    """Create the persistent url from a Query"""

    view_to_reverse = None

    def post(self, request):
        """Create a persistent query
        Args:
            request:

        Returns:

        """
        try:
            # get parameter
            query_id = request.POST.get("queryId", None)

            # get the matching query
            query = query_api.get_by_id(query_id, request.user)

            # create the persistent query
            persistent_query = abstract_persistent_query_api.upsert(
                self._create_persistent_query(query),
                query.templates.all(),
                request.user,
            )
            # reverse to the url
            url_reversed = request.build_absolute_uri(reverse(self.view_to_reverse))
            # context
            return HttpResponse(
                json.dumps({"url": url_reversed + "?id=" + str(persistent_query.id)}),
                content_type="application/javascript",
            )
        except DoesNotExist:
            return HttpResponseBadRequest("The query does not exist anymore.")
        except Exception as exception:
            return HttpResponseBadRequest(
                escape(str(exception)), content_type="application/javascript"
            )

    @staticmethod
    @abstractmethod
    def _create_persistent_query(query):
        """Create the persistent query

        Args:
            query:

        Returns:

        """
        raise NotImplementedError("_create_persistent_query method is not implemented.")


@method_decorator(login_required, name="dispatch")
class ContentPersistentQueryView(CommonView):
    """
    View persistent query content
    """

    template = (
        "core_explore_common_app/user/persistent_query/persistent_query_content.html"
    )

    def get(self, request, *args, **kwargs):
        """Gets persistent query

        Args:
            request:

        Returns:

        """

        try:
            # get persistent query id
            persistent_query_id = kwargs["persistent_query_id"]

            # get persistent query class name
            persistent_query_type = kwargs["persistent_query_type"]

            persistent_query_class = next(
                (
                    subclass
                    for subclass in AbstractPersistentQuery.get_subclasses()
                    if subclass.__name__ == persistent_query_type
                ),
                None,
            )

            # get persistent query
            persistent_query = abstract_persistent_query_api.get_by_id(
                persistent_query_class, persistent_query_id, request.user
            )
        except DoesNotExist:
            return HttpResponseBadRequest("The query does not exist.")
        except Exception:
            return HttpResponseBadRequest("Something wrong happened.")

        # create context
        content = json.loads(persistent_query.content)
        context = {"query": persistent_query, "content": json.dumps(content, indent=4)}
        assets = {
            "js": [
                {"path": "core_main_app/common/js/backtoprevious.js", "is_raw": True},
                {
                    "path": "core_main_app/libs/highlight/11.0.0/js/highlight.min.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/libs/highlight/11.0.0/js/init_highlight.js",
                    "is_raw": False,
                },
            ],
            "css": ["core_main_app/libs/highlight/11.0.0/css/atom-one-light.css"],
        }

        return self.common_render(
            request, self.template, assets=assets, context=context
        )
