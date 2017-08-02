""" REST views for the data API
"""
from urlparse import urljoin

from core_explore_common_app.components.result.models import Result
from django.core.urlresolvers import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.result.result import get_result_from_rest_data_response
from rest_framework import status
import core_main_app.components.data.api as data_api
import requests


@api_view(['GET'])
def get_result_from_data_id(request):
    """ Access data, Returns Result, Expects a data ID

    Args:
        request:

    Returns:

    """
    try:
        # get parameters
        data_id = request.GET.get('id', None)

        # if no data id given
        if data_id is None:
            content = {'message': "data id is missing"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # call api
        data = data_api.get_by_id(data_id, request.user)

        # Build a Result
        result = Result(title=data.title, xml_content=data.xml_content)

        # Serialize results
        return_value = ResultSerializer(result)

        # Returns the response
        return Response(return_value.data, status=status.HTTP_200_OK)

    except Exception as e:
        # if something went wrong, return an internal server error
        content = {'message': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
