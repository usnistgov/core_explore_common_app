""" Url router for the Explore Common application
"""
from django.conf.urls import url, include
from core_explore_common_app.views.user import ajax as user_ajax

urlpatterns = [
    url(r'^rest/', include('core_explore_common_app.rest.urls')),

    url(r'^get_local_data_source', user_ajax.get_local_data_source,
        name='core_explore_common_get_local_data_source'),

    url(r'^update-local-data-source', user_ajax.update_local_data_source,
        name='core_explore_common_update_local_data_source'),

    url(r'^data-sources-html', user_ajax.get_data_sources_html,
        name='core_explore_common_data_sources_html'),

    url(r'^data-source-results/(?P<query_id>\w+)/(?P<data_source_index>\w+)/(?P<page>\w+)',
        user_ajax.get_data_source_results,
        name='core_explore_common_data_source_results'),

    url(r'^data-source-results/(?P<query_id>\w+)/(?P<data_source_index>\w+)',
        user_ajax.get_data_source_results,
        name='core_explore_common_data_source_results'),
]
