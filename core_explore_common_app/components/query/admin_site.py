""" Custom admin site for the Query model
"""
from django.contrib import admin


class CustomQueryAdmin(admin.ModelAdmin):
    """CustomQueryAdmin"""

    readonly_fields = ["content", "templates", "creation_date"]
    exclude = ["data_sources"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Queries"""
        return False
