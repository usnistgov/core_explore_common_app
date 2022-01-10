""" Auto discovery of explore common app.
"""
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from core_explore_common_app.tasks import delete_old_queries


def init_periodic_tasks():
    """Create periodic tasks for the app and add them to a crontab schedule"""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        hour=0,
        minute=0,
    )
    try:
        PeriodicTask.objects.get(name=delete_old_queries.__name__)
    except ObjectDoesNotExist:
        PeriodicTask.objects.create(
            crontab=schedule,
            name=delete_old_queries.__name__,
            task="core_explore_common_app.tasks.delete_old_queries",
        )
