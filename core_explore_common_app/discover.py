""" Auto discovery of explore common app.
"""
import logging

from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from core_explore_common_app.tasks import delete_old_queries

logger = logging.getLogger(__name__)


def init_periodic_tasks():
    """Create periodic tasks for the app and add them to a crontab schedule"""
    try:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=0,
            minute=0,
        )
        PeriodicTask.objects.get(name=delete_old_queries.__name__)
    except ObjectDoesNotExist:
        PeriodicTask.objects.create(
            crontab=schedule,
            name=delete_old_queries.__name__,
            task="core_explore_common_app.tasks.delete_old_queries",
        )
    except Exception as exception:
        logger.error(str(exception))
