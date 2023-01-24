""" Utils for the OAI-PMH protocol
"""
from django.conf import settings


def is_oai_data_source(data_source):
    """Check if oai data source

    Args:
        data_source:

    Returns:

    """
    if (
        "core_explore_oaipmh_app" in settings.INSTALLED_APPS
        and "core_oaipmh_harvester_app" in settings.INSTALLED_APPS
    ):
        from core_oaipmh_harvester_app.components.oai_registry import (
            api as oai_registry_api,
        )

        return data_source["name"] in oai_registry_api.get_all().values_list(
            "name", flat=True
        )
    return False
