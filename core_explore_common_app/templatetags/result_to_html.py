""" Convert result to HTML
"""

import logging

from django import template as django_template

from core_explore_common_app.components.result.models import Result
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.templatetags.data_to_html import (
    _render_data_html,
    _get_template_html_rendering,
    _data_content_to_dict,
)

register = django_template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag(name="result_list_html")
def result_list_html(result):
    """result_list_html

    Args:
        result:

    Returns:

    """
    # if result is a Result object
    if isinstance(result, Result):
        # get template info
        template_info = result.template_info
        # get result content
        result_content = result.content
    # if result is a dict
    elif isinstance(result, dict):
        # get template info
        template_info = result.get("template_info", None)
        # get result content
        result_content = result["content"]
    # if result is unknown type, return None
    else:
        return None

    # if template info not provided, return None
    if not template_info:
        return None

    # get template id from template info
    template_id = template_info.get("id", None)
    # get template hash from template info
    template_hash = template_info.get("hash", None)
    # get template format from template info
    template_format = template_info.get("format", None)

    try:
        # get detail html rendering for this template
        template_html_rendering = _get_template_html_rendering(
            template_id=template_id,
            template_hash=template_hash,
            rendering_type="list",
        )
        # if template html rendering not set, return None
        if not template_html_rendering:
            return None
        # if result is not a dict
        if not isinstance(result_content, dict):
            result_content = _data_content_to_dict(
                result_content, template_format
            )
        # render result content with list rendering template
        return _render_data_html(template_html_rendering, result_content)
    except DoesNotExist:
        # no template html rendering found
        return None
    except Exception as e:
        logger.error(
            "An error occurred while rendering data to html: " + str(e)
        )
        return None
