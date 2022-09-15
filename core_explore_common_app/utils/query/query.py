"""Explore Common query utils
"""
import json

from django.urls import reverse
from django.utils import timezone
from requests import ConnectionError

from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.requests_utils.requests_utils import send_get_request

from core_explore_common_app import settings
from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.components.abstract_query.models import (
    Authentication,
    DataSource,
)
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.constants import LOCAL_QUERY_NAME, LOCAL_QUERY_URL
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.protocols.oauth2 import (
    send_post_request as oauth2_request,
)


def send(request, query, data_source_index, page):
    """

    Args:
        request:
        query:
        data_source_index:
        page:

    Returns:

    """
    try:
        # get data source to reach
        data_source = query.data_sources[data_source_index]
        # get serialized query to send to data source
        json_query = _serialize_query(query, data_source)
        # add page number to query url
        query_url = _get_paginated_url(data_source["url_query"], page)
        # send query to data source
        if data_source["authentication"]["auth_type"] == "session":
            response = send_get_request(
                query_url,
                data=json_query,
                cookies={"sessionid": request.session.session_key},
            )
        elif data_source["authentication"]["auth_type"] == "oauth2":
            response = oauth2_request(
                query_url,
                json_query,
                data_source["authentication"]["params"]["access_token"],
                session_time_zone=timezone.get_current_timezone(),
            )
        else:
            raise ExploreRequestError("Unknown authentication type.")

        # if got a response from data source
        if response.status_code == 200:
            # transform response to json
            json_response = response.json()
            # Build serializer
            results_serializer = ResultSerializer(
                data=json_response["results"], many=True
            )

            # Validate data
            results_serializer.is_valid(True)

            return json_response

        raise ExploreRequestError(
            f'Data source {data_source["name"]} '
            f"responded with status code {str(response.status_code)}."
        )
    except IndexError:
        raise ExploreRequestError("The selected data source is not available.")
    except ConnectionError:
        raise ExploreRequestError("Unable to contact the remote server.")
    except Exception as exception:
        raise ExploreRequestError(str(exception))


def add_local_data_source(request, query):
    """Add local data source to query

    Args:
        request:
        query:

    Returns:

    """
    # Add Local to the query as a data source
    data_source = create_local_data_source(request)
    query_api.add_data_source(query, data_source, request.user)


def create_local_data_source(request):
    """Create local datasource

    Args:
        request:

    Returns:
    """
    local_name = LOCAL_QUERY_NAME
    local_query_url = get_local_query_absolute_url(request)
    authentication = Authentication(auth_type="session")
    data_source = DataSource(
        name=local_name,
        url_query=local_query_url,
        authentication=authentication,
        order_by_field=",".join(DATA_SORTING_FIELDS),
    )

    if "core_linked_records_app" in settings.INSTALLED_APPS:
        data_source["capabilities"] = {
            "url_pid": request.build_absolute_uri(
                reverse("core_linked_records_app_query_local")
            )
        }

    return data_source


def get_local_query_absolute_url(request):
    """Return local query absolute URL.

    Args:
        request:
        query:

    Returns:
        String: Absolute URL

    """
    return request.build_absolute_uri(reverse(LOCAL_QUERY_URL))


# TODO: see if can be done using a Serializer
def _serialize_query(query, data_source):
    return {
        "query": query.content,
        "templates": json.dumps(
            [
                {"id": template.id, "hash": template.hash}
                for template in query.templates.all()
            ]
        ),
        "options": json.dumps(data_source["query_options"]),
        "order_by_field": data_source["order_by_field"],
    }


def _get_paginated_url(url, page):
    """Add a page number to the url

    Args:
        url:
        page:

    Returns:

    """
    return f"{url}/?page={page}"
