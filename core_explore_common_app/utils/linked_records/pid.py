""" Utils for PIDs
"""
from core_main_app.commons.exceptions import ApiError
from logging import getLogger

logger = getLogger(__name__)


def is_auto_set_pid_enabled(installed_apps, user, use_system_api=False):
    """Check if PID are available and enabled.

    Returns:
        bool - True if core_linked_records_app is installed and PID are activated.
    """
    if "core_linked_records_app" in installed_apps:
        if not use_system_api:
            from core_linked_records_app.components.pid_settings import (
                api as pid_settings_api,
            )

            return pid_settings_api.get(user).auto_set_pid
        else:
            from core_linked_records_app.system.pid_settings import (
                api as pid_settings_system_api,
            )

            return pid_settings_system_api.get().auto_set_pid
    return False


def get_pid_url(data, request):
    """Get pid url

    Args:
        data:
        request:

    Returns:

    """
    from core_linked_records_app.components.data import (
        api as pid_data_api,
    )

    try:
        return pid_data_api.get_pid_for_data(data.id, request)
    except ApiError as exc:
        # If there is an error with the PID, fallback to regular data url
        logger.warning(
            "An error occurred while retrieving PID url: %s",
            str(exc),
        )
        return None
