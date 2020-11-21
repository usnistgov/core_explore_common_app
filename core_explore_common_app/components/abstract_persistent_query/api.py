"""Persistent Query api
"""

from core_explore_common_app.access_control.api import can_write_persistent_query
from core_main_app.access_control.decorators import access_control


@access_control(can_write_persistent_query)
def upsert(persistent_query, user):
    """Saves or update persistent query

    Args:
        persistent_query:

    Returns:

    """
    return persistent_query.save()
