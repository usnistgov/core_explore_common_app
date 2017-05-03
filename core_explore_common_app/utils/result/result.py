"""Explore Common result utils
"""
from core_main_app.components.version_manager import api as version_manager_api


def get_template_info(template, include_template_id=True):
    """Gets template information
    Args:
        template: Template to get information from.
        include_template_id: Include the template id in the information

    Returns:
        Template information.

    """
    version_manager = version_manager_api.get_from_version(template)
    version_number = version_manager_api.get_version_number(version_manager, template.id)

    return {'id': template.id if include_template_id else '',
            'name': "{0} (Version {1})".format(version_manager.title,version_number),
            'hash': template.hash}
