""" REST views for the query API
"""

from django.urls import reverse

from core_explore_common_app import settings
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_common_app.utils.result import result as result_utils
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.utils.pagination.rest_framework_paginator.pagination import (
    StandardResultsSetPagination,
)


class ExecuteLocalQueryView(AbstractExecuteLocalQueryView):
    def build_response(self, data_list):
        """Build the paginated list of data

        Args:

            data_list: List of data

        Returns:

            Paginated list of data
        """
        # get paginator
        paginator = StandardResultsSetPagination()
        # get requested page from list of results
        page = paginator.paginate_queryset(data_list, self.request)

        # Get detail view base url (to be completed with data id)
        detail_url_base = reverse("core_main_app_data_detail")
        url_access_data = reverse("core_explore_common_app_get_result_from_data_id")
        url_permission_data = reverse("core_main_app_rest_data_permissions")

        # Build list of results
        results = []
        # Template info
        template_info = dict()
        # Init pid settings
        auto_set_pid = False
        if "core_linked_records_app" in settings.INSTALLED_APPS:
            from core_linked_records_app.components.pid_settings import (
                api as pid_settings_api,
            )

            auto_set_pid = pid_settings_api.get().auto_set_pid
        for data in page:
            # get data's template
            template_id = data.template_id
            # get and store data's template information
            if template_id not in template_info:
                template_info[template_id] = result_utils.get_template_info(
                    data.template
                )

            detail_url = "{0}?id={1}".format(detail_url_base, str(data.id))

            # Use the PID link if the app is installed and a PID is defined for the
            # document
            if "core_linked_records_app" in settings.INSTALLED_APPS:
                from core_linked_records_app.components.data import api as data_api

                if auto_set_pid:
                    pid_url = data_api.get_pids_for_data_list([data.id], self.request)

                    if len(pid_url) == 1:  # If a PID is defined for the document
                        detail_url = pid_url[0].replace(settings.SERVER_URI, "")

            results.append(
                Result(
                    title=data.title,
                    xml_content=data.xml_content,
                    template_info=template_info[template_id],
                    permission_url="{0}?ids={1}".format(
                        url_permission_data, f'%5B"{str(data.id)}"%5D'
                    ),
                    detail_url=detail_url,
                    access_data_url="{0}?id={1}".format(url_access_data, str(data.id)),
                    last_modification_date=data.last_modification_date,
                )
            )

        # serialize results
        serialized_results = ResultSerializer(results, many=True)
        # return http response
        return paginator.get_paginated_response(serialized_results.data)
