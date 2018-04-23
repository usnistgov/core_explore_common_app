"""Persistent Query api
"""


def upsert(persistent_query):
    """Saves or update persistent query

    Args:
        persistent_query:

    Returns:

    """
    return persistent_query.save()
