""" Explore Common App tasks
"""
import logging
from datetime import timedelta

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

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
            if query.id.generation_time
            < timezone.now() - timedelta(days=QUERIES_MAX_DAYS_IN_DATABASE)
        ]
        # remove old queries from database
        for query in old_queries:
            logger.info("Periodic task: delete query {}.".format(str(query.id)))
            query.delete()
    except Exception as e:
        logger.error(
            "An error occurred while deleting old queries ({}).".format(str(e))
        )
