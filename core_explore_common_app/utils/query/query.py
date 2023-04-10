"""Explore Common query utils
"""

import json

from django.utils import timezone
from requests import ConnectionError

from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.components.abstract_query.models import (
    Authentication,
    DataSource,
)
from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.protocols import oauth2
from core_main_app.settings import DATA_SORTING_FIELDS, SERVER_URI


def send(request, json_query, data_source, page):
    """

    Args:
        request:
        json_query:
        data_source:
        page:

    Returns:

    """
    try:
        # add page number to query url
        query_url = f"{data_source['url_query']}/?page={page}"
        # send query to data source
        if data_source["authentication"]["auth_type"] == "oauth2":
            response = oauth2.send_post_request(
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
            results_serializer.is_valid(raise_exception=True)

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


def create_local_data_source(request):
    """Create local datasource

    Args:
        request:

    Returns:
    """
    local_name = LOCAL_QUERY_NAME
    authentication = Authentication(auth_type="session")
    data_source = DataSource(
        name=local_name,
        url_query=SERVER_URI,
        authentication=authentication,
        order_by_field=",".join(DATA_SORTING_FIELDS),
    )

    return data_source


def is_local_data_source(data_source):
    """Check if local data source

    Args:
        data_source:

    Returns:

    """
    return (
        data_source["name"] == LOCAL_QUERY_NAME
        and data_source["url_query"] == SERVER_URI
    )


def serialize_query(query, data_source):
    """Serialize the query

    Args:
        query:
        data_source:

    Returns:

    """
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
