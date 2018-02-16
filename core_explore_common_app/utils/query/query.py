"""Explore Common query utils
"""
import json

import requests
from requests import ConnectionError

from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.protocols.oauth2 import send_post_request as oauth2_request


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
        query_url = _get_paginated_url(data_source.url_query, page)
        # send query to data source
        if data_source.authentication.type == "session":
            response = requests.get(query_url, data=json_query, cookies={"sessionid": request.session.session_key})
        elif data_source.authentication.type == "oauth2":
            response = oauth2_request(query_url, json_query, data_source.authentication.params['access_token'])
        else:
            raise ExploreRequestError("Unknown authentication type.")

        # if got a response from data source
        if response.status_code == 200:
            # transform response to json
            json_response = json.loads(response.text)
            # Build serializer
            results_serializer = ResultSerializer(data=json_response['results'], many=True)

            # Validate data
            results_serializer.is_valid(True)

            return json_response
        else:
            raise ExploreRequestError("Data source {0} responded with status code {1}.".
                                      format(data_source.name, str(response.status_code)))
    except ConnectionError:
        raise ExploreRequestError("Unable to contact the remote server.")
    except Exception, e:
        raise ExploreRequestError(e.message)


# TODO: see if can be done using a Serializer
def _serialize_query(query, data_source):
    return {
        "query": query.content,
        "templates": json.dumps([{'id': str(template.id), 'hash': template.hash} for template in query.templates]),
        "options": json.dumps(data_source.query_options),
    }


def _get_paginated_url(url, page):
    """Add a page number to the url

    Args:
        url:
        page:

    Returns:

    """
    return "{0}/?page={1}".format(url, page)
