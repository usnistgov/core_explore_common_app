""" Explore Common App tasks
"""
import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from core_explore_common_app.settings import QUERIES_MAX_DAYS_IN_DATABASE
from core_explore_common_app.system.api import get_all_queries

logger = logging.getLogger(__name__)


@shared_task
def delete_old_queries():
    """Every day at midnight, delete older queries.

    Returns:

    """
    try:
        # get older queries
        old_queries = [
            query
            for query in get_all_queries()
            if query.creation_date
            < timezone.now() - timedelta(days=QUERIES_MAX_DAYS_IN_DATABASE)
        ]
        # remove old queries from database
        for query in old_queries:
            logger.info("Periodic task: delete query %s.", str(query.id))
            query.delete()
    except Exception as exception:
        logger.error(
            "An error occurred while deleting old queries (%s).", str(exception)
        )
