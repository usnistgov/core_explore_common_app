""" Abstract Persistent Query model
"""
from django.db import models

from core_explore_common_app.components.abstract_query.models import (
    AbstractQuery,
)


class AbstractPersistentQuery(AbstractQuery):
    """Abstract Persistent Query"""

    name = models.CharField(unique=True, blank=True, max_length=200, null=True)

    class Meta:
        """Meta"""

        abstract = True

    @staticmethod
    def get_subclasses():
        """
        Returns: list of subclasses


        """

        return AbstractPersistentQuery.__subclasses__()
