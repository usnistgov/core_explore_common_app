"""Explore Common result utils
"""
import json

from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import (
    ResultSerializer,
    ResultBaseSerializer,
)


def get_template_info(template, include_template_id=True):
    """Gets template information
    Args:
        template: Template to get information from.
        include_template_id: Include the template id in the information

    Returns:
        Template information.

    """
    # Here the id need to be set anyway because is expected by the serializer
    return_value = {
        "id": template.id if include_template_id else "",
        "name": template.display_name,
        "hash": template.hash,
        "format": template.format,
    }

    return return_value


def get_result_from_rest_data_response(response):
    """Returns result object from data rest response

    Args:
        response:

    Returns:

    """
    # data serialization
    result_serialized = ResultBaseSerializer(data=json.loads(response.text))
    # Validate data
    result_serialized.is_valid(raise_exception=True)
    # Build a Result
    result = Result(
        title=result_serialized.data["title"],
        content=result_serialized.data["content"],
    )
    # Serialize results
    return_value = ResultSerializer(result)
    # Returns the response
    return return_value.data
