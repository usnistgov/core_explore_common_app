""" REST views for the data API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core_main_app.commons import exceptions
import core_main_app.components.data.api as data_api
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer


@api_view(["GET"])
def get_result_from_data_id(request):
    """Retrieve a Result

    Parameters:

        {
            "id": data_id
        }

    Args:

        request: HTTP request

    Returns:

        - code: 200
          content: Result
        - code: 500
          content: Internal server error
    """
    try:
        # get parameters
        data_id = request.GET.get("id", None)

        # if no data id given
        if data_id is None:
            content = {"message": "data id is missing"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # call api
        data = data_api.get_by_id(data_id, request.user)

        # Build a Result
        result = Result(title=data.title, xml_content=data.xml_content)

        # Serialize results
        return_value = ResultSerializer(result)

        # Returns the response
        return Response(return_value.data, status=status.HTTP_200_OK)

    except exceptions.DoesNotExist as does_not_exist_exception:
        content = {"message": str(does_not_exist_exception)}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as exception:
        # if something went wrong, return an internal server error
        content = {"message": str(exception)}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
