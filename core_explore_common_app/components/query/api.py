""" Query api
"""

from core_explore_common_app import settings
from core_explore_common_app.access_control.api import can_read, can_access
from core_explore_common_app.components.query.models import Query
from core_explore_common_app.settings import (
    EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY,
)
from core_explore_common_app.utils.query.query import (
    create_local_data_source,
    is_local_data_source,
)
from core_main_app.access_control.decorators import access_control
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.query.constants import VISIBILITY_OPTION


@access_control(can_access)
def upsert(query, user):
    """Saves or uploads query

    Args:
        query:
        user:

    Returns:

    """
    query.save()
    return query


def create_default_query(request, template_ids):
    """create a new Query object

    Args:
        request:
        template_ids:

    Returns:

    """
    # create new query object
    query = Query(user_id=str(request.user.id))
    if EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY:
        # add the local data source by default
        add_local_data_source(request, query)
    # add a default empty query content
    query.content = "{}"
    # Save query in database
    upsert(query, request.user)
    # Set list of templates
    query.templates.set(template_ids)
    return query


def add_local_data_source(request, query):
    """Add local data source to query

    Args:
        request:
        query:

    Returns:

    """
    # Add Local to the query as a data source
    data_source = create_local_data_source(request)
    # Add data source to query (with access control)
    add_data_source(query, data_source, request.user)


@access_control(can_read)
def get_by_id(id_query, user):
    """Returns a query with the given id

    Args:
        id_query:
        user:

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
            query, data_source["name"], data_source["url_query"], user
        )
        # already present return query
        return query
    except DoesNotExist:
        # add data source to query if not present
        query.data_sources.append(data_source)
        # update query
        upsert(query, user)
        return query


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
    upsert(query, user)
    return query


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
        if is_local_data_source(data_source):
            # set visibility to public
            data_source["query_options"] = {
                VISIBILITY_OPTION: settings.QUERY_VISIBILITY
            }
            break
