"""Url router for the administration site
"""
from django.contrib import admin

from core_explore_common_app.components.query.admin_site import (
    CustomQueryAdmin,
)
from core_explore_common_app.components.query.models import Query

admin.site.register(Query, CustomQueryAdmin)
