"""Result models
"""
from django.db import models


class Result(models.Model):
    """Result class"""

    title = models.CharField(blank=False, max_length=200)
    xml_content = models.TextField(blank=False)
    template_info = models.JSONField(default=dict)
    permission_url = models.CharField(blank=True, null=True, max_length=200)
    detail_url = models.CharField(blank=True, null=True, max_length=200)
    access_data_url = models.CharField(blank=True, null=True, max_length=200)
    last_modification_date = models.DateTimeField(blank=True, default=None)
