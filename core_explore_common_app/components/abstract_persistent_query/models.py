""" Abstract Persistent Query model
"""
from core_explore_common_app.components.abstract_query.models import AbstractQuery


class AbstractPersistentQuery(AbstractQuery):
    """ Abstract Persistent Query
    """

    meta = {
        'abstract': True,
    }
