""" Query api
"""
from core_explore_common_app import settings
from core_explore_common_app.access_control.api import can_read, can_access
from core_explore_common_app.components.query.models import Query
from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.query.constants import VISIBILITY_OPTION


@access_control(can_access)
def upsert(query, user):
    """Saves or uploads query

    Args:
        query:

    Returns:

    """
    return query.save()


@access_control(can_read)
def get_by_id(id_query, user):
    """Returns a query with the given id

    Args:
        id_query:

    Returns:

    """
    return Query.get_by_id(id_query)


@access_control(can_access)
def add_data_source(query, data_source, user):
    """Adds a data source to the query

    Args:
        query:
        data_source:
        user:

    Returns:

    """
    try:
        # check if data source is already present
        get_data_source_by_name_and_url_query(
            query, data_source.name, data_source.url_query, user
        )
        # already present return query
        return query
    except DoesNotExist:
        # add data source to query if not present
        query.data_sources.append(data_source)
        # update query
        return upsert(query, user)


@access_control(can_access)
def remove_data_source(query, data_source, user):
    """Removes a data source from the query

    Args:
        query:
        data_source:
        user:

    Returns:

    """
    query.data_sources.remove(data_source)
    return upsert(query, user)


@access_control(can_access)
def get_data_source_by_name_and_url_query(query, name, url_query, user):
    """Returns a data source from given name and url of query

    Args:
        query:
        name:
        url_query:
        user:

    Returns:

    """
    return query.get_data_source_by_name_and_url_query(name, url_query)


@access_control(can_access)
def set_visibility_to_query(query, user):
    """Set visibility with the visibility defined in settings

    Args:
        query:
        user:

    Returns:

    """
    # Set visibility option for local data source
    for data_source in query.data_sources:
        # find local data source
        if data_source.name == LOCAL_QUERY_NAME:
            # set visibility to public
            data_source.query_options = {VISIBILITY_OPTION: settings.QUERY_VISIBILITY}
            break
