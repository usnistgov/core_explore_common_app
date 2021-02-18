""" Abstract Persistent Query model
"""
from core_explore_common_app.components.abstract_query.models import AbstractQuery
from django_mongoengine import fields


class AbstractPersistentQuery(AbstractQuery):
    """Abstract Persistent Query"""

    name = fields.StringField(sparse=True, unique=True, blank=True)
    meta = {
        "abstract": True,
    }

    @staticmethod
    def get_subclasses():
        """
        Returns: list of subclasses


        """

        return AbstractPersistentQuery.__subclasses__()
