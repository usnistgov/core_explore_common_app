"""System API
"""
from core_explore_common_app.components.query.models import Query


def get_all_queries():
    """Return all queries.

    Returns:

    """
    return Query.objects.all()
