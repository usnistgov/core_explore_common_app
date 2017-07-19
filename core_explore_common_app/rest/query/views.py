""" REST views for the query API
"""
import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.pagination.rest_framework_paginator.pagination import \
    StandardResultsSetPagination
from core_explore_common_app.utils.query.mongo.query_builder import QueryBuilder
from core_explore_common_app.utils.result import result as result_utils
from core_main_app.components.data import api as data_api


class ExecuteLocalQueryView(APIView):
    request = None
    sub_document_root = 'dict_content'

    def get(self, request):
        """Execute query on local instance and return results

        Args:
            request:

        Returns:

        """
        try:
            # get query and templates
            query = request.data.get('query', None)
            templates = request.data.get('templates', [])
            # keep request info
            self.request = request

            if query is not None:
                # prepare query
                raw_query = self.build_query(query, templates)
                # execute query
                data_list = self.execute_raw_query(raw_query)
                # build and return response
                return self.build_response(data_list)
            else:
                content = {'message': 'Expected parameters not provided.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def build_query(self, query, templates):
        """ Build the raw query.
        Args:
            query:
            templates:

        Returns:
            The raw query.

        """
        # build query builder
        query_builder = QueryBuilder(query, self.sub_document_root)
        # update the criteria with templates information
        templates = json.loads(templates)
        if len(templates) > 0:
            list_template_ids = [template['id'] for template in templates]
            query_builder.add_list_templates_criteria(list_template_ids)
        # get raw query
        return query_builder.get_raw_query()

    def execute_raw_query(self, raw_query):
        """ Execute the raw query in database.
        Args:
            raw_query: Query to execute.

        Returns:
            Results of the query.

        """
        return data_api.execute_query(raw_query, self.request.user)

    def build_response(self, data_list):
        """ Build the paginated response.

        Args:
            data_list: List of data.

        Returns:
            The response.

        """
        # get paginator
        paginator = StandardResultsSetPagination()
        # get requested page from list of results
        page = paginator.paginate_queryset(data_list, self.request)

        # FIXME: See if can use reverse to include data id, and avoid format
        # Get detail view base url (to be completed with data id)
        detail_url_base = reverse("core_main_app_data_detail")
        url_access_data = reverse("core_explore_common_app_get_result_from_data_id")

        # Build list of results
        results = []
        # Template info
        template_info = dict()
        for data in page:
            # get data's template
            template = data.template
            # get and store data's template information
            if template not in template_info:
                template_info[template] = result_utils.get_template_info(template)

            results.append(Result(title=data.title,
                                  xml_content=data.xml_content,
                                  template_info=template_info[template],
                                  detail_url="{0}?id={1}".format(detail_url_base, str(data.id)),
                                  access_data_url="{0}?id={1}".format(url_access_data,
                                                                      str(data.id))
                                  )
                           )

        # serialize results
        serialized_results = ResultSerializer(results, many=True)
        # return http response
        return paginator.get_paginated_response(serialized_results.data)
