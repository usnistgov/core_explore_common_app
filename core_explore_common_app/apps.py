""" Core explore common apps config
"""
import sys

from django.apps import AppConfig


class CoreExploreCommonAppConfig(AppConfig):
    """Explore common configuration"""

    name = "core_explore_common_app"
    verbose_name = "Core Explore Common App"

    def ready(self):
        """Run once at startup"""
        if "migrate" not in sys.argv:
            from core_explore_common_app import discover

            discover.init_periodic_tasks()
