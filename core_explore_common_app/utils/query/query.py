"""Explore Common query utils
"""
from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.protocols.oauth2 import send_post_request as oauth2_request
import requests
import json


def send(query, data_source_index):
    """

    Args:
        query:
        data_source_index:

    Returns:

    """
    try:
        # get data source to reach
        data_source = query.data_sources[data_source_index]
        # get serialized query to send to data source
        json_query = _serialize_query(query, data_source)
        # send query to data source
        if data_source.authentication.type == "session":
            response = requests.post(data_source.url_query, data=json_query)
        elif data_source.authentication.type == "oauth2":
            response = oauth2_request(data_source.url_query, json_query,
                                      data_source.authentication.params['access_token'])
        else:
            raise ExploreRequestError("Unknown authentication type.")

        # if got a response from data source
        if response.status_code == 200:
            # Build serializer
            results_serializer = ResultSerializer(data=json.loads(response.text), many=True)

            # Validate data
            results_serializer.is_valid(True)

            return results_serializer.data
        else:
            raise ExploreRequestError("Data source {0} responded with status code {1}.".
                                      format(data_source.name, str(response.status_code)))
    except Exception, e:
        raise ExploreRequestError(e.message)


# TODO: see if can be done using a Serializer
def _serialize_query(query, data_source):
    return {
        "query": query.content,
        "templates": json.dumps([{'id': str(template.id), 'hash': template.hash} for template in query.templates]),
        "options": json.dumps(data_source.query_options)
    }
