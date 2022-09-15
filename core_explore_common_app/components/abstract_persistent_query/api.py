"""Persistent Query api
"""

from core_main_app.access_control.decorators import access_control
from core_explore_common_app.access_control.api import (
    can_write_persistent_query,
    can_read_persistent_query,
)


@access_control(can_write_persistent_query)
def upsert(persistent_query, templates, user):
    """Saves or update persistent query

    Args:
        persistent_query:
        templates:
        user:

    Returns:

    """
    persistent_query.save()
    persistent_query.templates.set(templates)
    return persistent_query


@access_control(can_read_persistent_query)
def get_all_persistent_queries(persistent_query_class, user):
    """Get all persistent queries

    Args:
        persistent_query_class:
        user:

    Returns:


    """

    return persistent_query_class.get_all()


@access_control(can_read_persistent_query)
def get_all_persistent_queries_by_user(persistent_query_class, user):
    """Get all persistent queries by user

    Args:
        persistent_query_class:
        user:

    Returns:


    """

    return persistent_query_class.get_all_by_user(user.id)


def get_none(persistent_query):
    """Returns None object, used by persistent query

    Args:
        persistent_query:

    Returns:


    """

    return persistent_query.get_none()


@access_control(can_read_persistent_query)
def get_by_id(persistent_query_class, persistent_query_id, user):
    """Return the Persistent Query with the given id

    Args:
        persistent_query_class:
        persistent_query_id:
        user:
    Returns:

    """
    return persistent_query_class.get_by_id(persistent_query_id)


@access_control(can_write_persistent_query)
def set_name(persistent_query, name, user):
    """Renames the Persistent Query

    Args:
        persistent_query:
        name:
        user:
    Returns:

    """
    persistent_query.name = name
    persistent_query.save()


@access_control(can_write_persistent_query)
def delete(persistent_query, user):
    """Deletes the Persistent Query.


    Args:

        persistent_query:

        user:

    """

    persistent_query.delete()
