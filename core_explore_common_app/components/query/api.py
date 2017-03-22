"""Query api
"""
from core_explore_common_app.components.query.models import Query
from core_main_app.commons.exceptions import DoesNotExist


def upsert(query):
    """Saves or uploads query

    Args:
        query:

    Returns:

    """
    return query.save()


def get_by_id(id_query):
    """Returns a query with the given id

    Args:
        id_query:

    Returns:

    """
    return Query.get_by_id(id_query)


def add_data_source(query, data_source):
    """Adds a data source to the query

    Args:
        query:
        data_source:

    Returns:

    """
    try:
        # check if data source is already present
        get_data_source_by_name_and_url_query(query, data_source.name, data_source.url_query)
        # already present return query
        return query
    except DoesNotExist:
        # add data source to query if not present
        query.data_sources.append(data_source)
        # update query
        return upsert(query)


def remove_data_source(query, data_source):
    """Removes a data source from the query

    Args:
        query:
        data_source:

    Returns:

    """
    query.data_sources.remove(data_source)
    return upsert(query)


def get_data_source_by_name_and_url_query(query, name, url_query):
    """Returns a data source from given name and url of query

    Args:
        query:
        name:
        url_query:

    Returns:

    """
    return query.get_data_source_by_name_and_url_query(name, url_query)
