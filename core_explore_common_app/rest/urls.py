"""Url router for the REST API
"""
from django.conf.urls import url
from core_explore_common_app.rest.query import views as query_views


urlpatterns = [
    url(r'^local-query', query_views.execute_local_query,
        name='core_explore_common_local_query'),
]
