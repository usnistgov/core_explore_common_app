""" Abstract Query model
"""

from django.db import models

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.template.models import Template

AUTH_TYPES = ("session", "oauth2")


class Authentication(dict):
    """Authentication class"""

    def __init__(self, auth_type="", params=None):
        if auth_type not in AUTH_TYPES:
            raise CoreError("Invalid AUTH_TYPE.")
        dict.__init__(
            self, auth_type=auth_type, params=params if params else dict()
        )


class DataSource(dict):
    """Data Source class"""

    def __init__(
        self,
        name,
        url_query,
        query_options=None,
        authentication=None,
        order_by_field=None,
        capabilities=None,
    ):
        dict.__init__(
            self,
            name=name,
            url_query=url_query,
            query_options=query_options if query_options else dict(),
            authentication=authentication if authentication else dict(),
            order_by_field=order_by_field if order_by_field else "",
            capabilities=capabilities if capabilities else dict(),
        )


class AbstractQuery(models.Model):
    """Abstract Query"""

    user_id = models.CharField(blank=False, max_length=200)
    content = models.TextField(blank=True, null=True)
    templates = models.ManyToManyField(
        Template, blank=True, default=[], symmetrical=False
    )
    data_sources = models.JSONField(blank=True, default=list)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta"""

        abstract = True
