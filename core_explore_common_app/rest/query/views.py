""" REST views for the query API
"""
from django.core.urlresolvers import reverse
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.query.mongo.query_builder import QueryBuilder
from core_main_app.components.data.api import execute_query
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core_explore_common_app.utils.result import result as result_utils
import json


@api_view(['POST'])
def execute_local_query(request):
    """Executes query on local instance and returns results

    Args:
        request:

    Returns:

    """
    try:
        # get query
        query = request.POST.get('query', None)

        if query is not None:
            # build query builder
            query_builder = QueryBuilder(query, 'dict_content')

            # update the criteria with templates information
            if 'templates' in request.POST:
                templates = json.loads(request.POST['templates'])
                if len(templates) > 0:
                    list_template_ids = [template['id'] for template in templates]
                    query_builder.add_list_templates_criteria(list_template_ids)

            # get raw query
            raw_query = query_builder.get_raw_query()

            # execute query
            data_list = execute_query(raw_query)

            # FIXME: See if can use reverse to include data id, and avoid format
            # Get detail view base url (to be completed with data id)
            detail_url_base = reverse("core_main_app_data_detail")

            # Build list of results
            results = []
            # Template info
            template_info = dict()
            for data in data_list:
                # get data's template
                template = data.template
                # get and store data's template information
                if template not in template_info:
                    template_info[template] = result_utils.get_template_info(template)

                results.append(Result(title=data.title,
                                      xml_content=data.xml_file,
                                      template_info=template_info[template],
                                      detail_url="{0}?id={1}".format(detail_url_base, str(data.id))
                                      )
                               )
            # Serialize results
            return_value = ResultSerializer(results, many=True)

            return Response(return_value.data, status=status.HTTP_200_OK)
        else:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
