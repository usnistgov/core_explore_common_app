"""AJAX Explore common user views
"""
import json
import math
from os.path import join

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader

from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Authentication, DataSource
from core_explore_common_app.settings import DATA_SOURCES_EXPLORE_APPS, RESULTS_PER_PAGE
from core_explore_common_app.settings import INSTALLED_APPS
from core_explore_common_app.utils.query.query import send as send_query
from core_main_app.utils.pagination.rest_framework_paginator.rest_framework_paginator import get_page_number


def get_local_data_source(request):
    """ Ajax method to get the local data source

    Args:
        request:

    Returns:

    """
    try:
        id_query = request.GET.get('query_id', None)
        local_query_url = request.GET.get('local_query_url', None)

        if id_query is not None:
            # Get query from id
            query = query_api.get_by_id(id_query)

            local_name = "Local"
            local_query_url = request.build_absolute_uri(reverse(local_query_url))

            context_params = {
                'enabled': True,
                'selected': False,
            }
            if len(DATA_SOURCES_EXPLORE_APPS) == 0:
                _add_local_data_source(query, local_name, local_query_url)
                context_params['enabled'] = False

            # check query to see if local data source was selected
            for data_source in query.data_sources:
                if data_source.name == local_name and data_source.url_query == local_query_url:
                    context_params['selected'] = True

            context = {}
            context.update(request)
            context.update(context_params)
            template = loader.get_template('core_explore_common_app/user/selector/local_content.html')
            html_data_source = template.render(context)
            return HttpResponse(html_data_source)
        else:
            return HttpResponseBadRequest("Expected query_id parameter is missing.")
    except Exception as e:
        return HttpResponseBadRequest("An unexpected error occurred while getting local data source selector.")


def update_local_data_source(request):
    """ Ajax method to update query with local data source

    Args:
        request:

    Returns:

    """
    try:
        query_id = request.GET['query_id']
        selected = json.loads(request.GET['selected'])
        local_query_url = request.GET.get('local_query_url', None)

        # Get query from id
        query = query_api.get_by_id(query_id)
        local_name = "Local"
        local_query_url = request.build_absolute_uri(reverse(local_query_url))

        if selected:
            # Local data source is selected, add it to the query as a data source
            _add_local_data_source(query, local_name, local_query_url)
        else:
            # Local data source is not selected, remove it from the query
            data_source = query_api.get_data_source_by_name_and_url_query(query, local_name, local_query_url)
            query_api.remove_data_source(query, data_source)

        return HttpResponse()
    except Exception as e:
        return HttpResponseBadRequest(e.message)


def get_data_sources_html(request):
    """Gets data sources html for results

    Args:
        request:

    Returns:

    """
    try:
        # get query id
        query_id = request.GET["query_id"]

        # get query results
        query = query_api.get_by_id(query_id)

        # set query in context
        context = {}
        context.update(request)
        context.update({
            'query': query
        })

        # render html results
        html_template = loader.get_template(
            join('core_explore_common_app', 'user', 'results', 'data_sources_results.html'))
        html_results_holders = html_template.render(context)

        response_dict = {'results': html_results_holders}
        return HttpResponse(json.dumps(response_dict), content_type='application/json')
    except Exception, e:
        return HttpResponseBadRequest(e.message)


def get_data_source_results(request, query_id, data_source_index, page=1):
    """Gets results from a data source

    Args:
        request:
        query_id:
        data_source_index:
        page:

    Returns:

    """
    try:
        # get query
        query = query_api.get_by_id(query_id)

        # send query, and get results from data source
        results = send_query(request, query, int(data_source_index), page)

        # set results in context
        context_data = {
            'results': results['results'],
            'query_id': query_id,
            'data_source_index': data_source_index,
            'pagination': {
                'number': int(page),
                'paginator': {'num_pages': int(math.ceil(float(results['count']) / RESULTS_PER_PAGE))},
                'has_other_pages': results['count'] > RESULTS_PER_PAGE,
                'previous_page_number': get_page_number(results['previous']),
                'next_page_number': get_page_number(results['next']),
                'has_previous': get_page_number(results['previous']) is not None,
                'has_next': get_page_number(results['next']) >
                            int(math.ceil(float(results['count']) / RESULTS_PER_PAGE)),
            },
            'exporter_app': 'core_exporters_app' in INSTALLED_APPS
        }

        # create context
        context = {}
        context.update(request)
        context.update(context_data)

        # generate html with context
        html_template = loader.get_template(join('core_explore_common_app', 'user', 'results',
                                                 'data_source_results.html'))
        # render html
        results_html = html_template.render(context)
        # set response with html results
        response_dict = {'results': results_html, 'nb_results': results['count']}
        return HttpResponse(json.dumps(response_dict), content_type='application/json')
    except ExploreRequestError, ex:
        return HttpResponseBadRequest("An error occurred while sending the query: " + ex.message)
    except Exception, e:
        return HttpResponseBadRequest("An unexpected error occurred: " + e.message)


def _add_local_data_source(query, local_name, local_query_url):
    """Adds local data source to query

    Args:
        query:
        local_name:
        local_query_url:

    Returns:

    """
    # Local data source is selected, add it to the query as a data source
    authentication = Authentication(type='session')
    data_source = DataSource(name=local_name,
                             url_query=local_query_url,
                             authentication=authentication)
    query_api.add_data_source(query, data_source)
