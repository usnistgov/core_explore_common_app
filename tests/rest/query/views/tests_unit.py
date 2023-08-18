""" Unit tests for local query views
"""

from unittest.mock import patch, MagicMock

from django.core import paginator as django_paginator
from django.test import SimpleTestCase, override_settings
from django.test import tag

from core_explore_common_app.rest.query import views as query_views
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.pagination.mongoengine_paginator import (
    paginator as mongo_paginator,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import (
    create_mock_request,
)


class TestExecuteLocalQuery(SimpleTestCase):
    """TestExecuteLocalQuery"""

    @patch("core_main_app.components.data.api.execute_json_query")
    def test_execute_local_query_returns_page_of_results(
        self, mock_execute_json_query
    ):
        """test_execute_local_query_returns_page_of_results"""
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {"query": {}}
        mock_request = create_mock_request(user=mock_user)
        mock_queryset = MagicMock()
        mock_execute_json_query.return_value = mock_queryset

        # Act
        page = query_views.execute_local_query(
            query_data=mock_query_data, page=1, request=mock_request
        )

        # Assert
        self.assertTrue(isinstance(page, django_paginator.Page))
        self.assertTrue(isinstance(page.paginator, django_paginator.Paginator))

    @patch("core_main_app.components.workspace.api.get_all_public_workspaces")
    @patch("core_main_app.components.data.api.execute_json_query")
    def test_execute_local_query_with_params_returns_page_of_results(
        self, mock_execute_json_query, mock_get_all_public_workspaces
    ):
        """test_execute_local_query_returns_page_of_results"""
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {
            "query": {},
            "templates": '[{"id": 1}]',
            "title": "test",
            "options": '{"visibility": "public"}',
        }
        mock_request = create_mock_request(user=mock_user)
        mock_queryset = MagicMock()
        mock_execute_json_query.return_value = mock_queryset
        mock_workspaces_response = MagicMock()
        mock_workspaces_response.values_list.return_value = [1]
        mock_get_all_public_workspaces.return_value = mock_workspaces_response

        # Act
        page = query_views.execute_local_query(
            query_data=mock_query_data, page=1, request=mock_request
        )

        # Assert
        self.assertTrue(isinstance(page, django_paginator.Page))
        self.assertTrue(mock_get_all_public_workspaces.called)

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.data.api.execute_json_query")
    def test_execute_local_query_returns_mongo_page_of_results(
        self, mock_execute_json_query
    ):
        """test_execute_local_query_returns_mongo_page_of_results"""
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {"query": {}}
        mock_request = create_mock_request(user=mock_user)
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        mock_execute_json_query.return_value = mock_queryset

        # Act
        page = query_views.execute_local_query(
            query_data=mock_query_data, page=1, request=mock_request
        )

        # Assert
        self.assertTrue(isinstance(page, django_paginator.Page))
        self.assertTrue(
            isinstance(page.paginator, mongo_paginator.MongoenginePaginator)
        )

    def test_execute_local_query_none_raises_api_error(self):
        """test_execute_local_query_none_raises_api_error"""
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {}
        mock_request = create_mock_request(user=mock_user)

        # Act + Assert
        with self.assertRaises(ApiError):
            query_views.execute_local_query(
                query_data=mock_query_data, page=1, request=mock_request
            )


class TestFormatLocalResults(SimpleTestCase):
    """TestFormatLocalResults"""

    def test_format_local_empty_results_returns_empty_list(
        self,
    ):
        """test_format_local_empty_results_returns_empty_list

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_results = MagicMock()
        mock_results.object_list = []
        mock_request = create_mock_request(user=mock_user)

        # Act
        results = query_views.format_local_results(
            results=mock_results, request=mock_request
        )

        # Assert
        self.assertIsInstance(results, list)

    @override_settings(INSTALLED_APPS=[])
    def test_format_local_results_returns_list(
        self,
    ):
        """test_format_local_results_returns_list

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_data = MagicMock()
        mock_data.template_id = 1
        mock_template = MagicMock()
        mock_template.id = 1
        mock_template.name = "template_name"
        mock_data.template = mock_template
        mock_results = MagicMock()
        mock_results.object_list = [mock_data]
        mock_request = create_mock_request(user=mock_user)

        # Act
        results = query_views.format_local_results(
            results=mock_results, request=mock_request
        )

        # Assert
        self.assertIsInstance(results, list)
        self.assertTrue(len(results), 1)

    @patch(
        "core_explore_common_app.utils.linked_records.pid.is_auto_set_pid_enabled"
    )
    @patch("core_explore_common_app.utils.linked_records.pid.get_pid_url")
    def test_format_local_results_with_pid_returns_list(
        self, mock_get_pid_url, mock_auto_set_pid_enabled
    ):
        """test_format_local_results_with_pid_returns_list

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_data = MagicMock()
        mock_data.template_id = 1
        mock_template = MagicMock()
        mock_template.id = 1
        mock_template.name = "template_name"
        mock_data.template = mock_template
        mock_results = MagicMock()
        mock_results.object_list = [mock_data]
        mock_request = create_mock_request(user=mock_user)

        mock_get_pid_url.return_value = None
        mock_auto_set_pid_enabled.return_value = True

        # Act
        results = query_views.format_local_results(
            results=mock_results, request=mock_request
        )

        # Assert
        self.assertIsInstance(results, list)
        self.assertTrue(len(results), 1)
