""" Unit tests for Explore Common REST API
"""

from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase, override_settings

from core_explore_common_app.rest.query import views as query_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import (
    create_mock_request,
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
        "core_explore_common_app.utils.linked_records.pid.auto_set_pid_enabled"
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
