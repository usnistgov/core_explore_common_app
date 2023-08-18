""" PID utils test class
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_explore_common_app.utils.linked_records.pid import (
    is_auto_set_pid_enabled,
    get_pid_url,
)
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestAutoSetPidEnabled(TestCase):
    """TestAutoSetPidEnabled"""

    @patch("core_linked_records_app.components.pid_settings.api.get")
    def test_auto_set_pid_enabled_returns_true_if_installed_and_enabled(
        self, mock_get
    ):
        """test_auto_set_pid_enabled_returns_true_if_installed_and_enabled

        Returns:

        """
        # Arrange
        mock_get_response = MagicMock()
        mock_get_response.auto_set_pid = True
        mock_get.return_value = mock_get_response
        mock_user = create_mock_user("1")

        # Act + Assert
        self.assertTrue(
            is_auto_set_pid_enabled(
                installed_apps=["core_main_app", "core_linked_records_app"],
                user=mock_user,
            )
        )

    @patch("core_linked_records_app.components.pid_settings.api.get")
    def test_auto_set_pid_enabled_returns_false_if_installed_and_disabled(
        self, mock_get
    ):
        """test_auto_set_pid_enabled_returns_false_if_installed_and_disabled

        Returns:

        """
        # Arrange
        mock_get_response = MagicMock()
        mock_get_response.auto_set_pid = False
        mock_get.return_value = mock_get_response
        mock_user = create_mock_user("1")

        # Act + Assert
        self.assertFalse(
            is_auto_set_pid_enabled(
                installed_apps=["core_main_app", "core_linked_records_app"],
                user=mock_user,
            )
        )

    @patch("core_linked_records_app.components.pid_settings.api.get")
    def test_auto_set_pid_enabled_returns_false_if_not_installed(
        self, mock_get
    ):
        """test_auto_set_pid_enabled_returns_false_if_installed_and_disabled

        Returns:

        """
        # Arrange
        mock_get_response = MagicMock()
        mock_get_response.auto_set_pid = False
        mock_get.return_value = mock_get_response
        mock_user = create_mock_user("1")

        # Act + Assert
        self.assertFalse(
            is_auto_set_pid_enabled(
                installed_apps=["core_main_app"], user=mock_user
            )
        )

    @patch("core_linked_records_app.system.pid_settings.api.get")
    def test_auto_set_pid_calls_system_api_when_set(self, mock_system_get):
        """test_auto_set_pid_calls_system_api_when_set

        Returns:

        """
        # Arrange
        mock_get_response = MagicMock()
        mock_get_response.auto_set_pid = False
        mock_system_get.return_value = mock_get_response
        mock_user = create_mock_user("1")

        # Act
        is_auto_set_pid_enabled(
            installed_apps=["core_main_app", "core_linked_records_app"],
            user=mock_user,
            use_system_api=True,
        )

        # Assert
        self.assertTrue(mock_system_get.called)


class TestGetPidUrl(TestCase):
    """TestGetPidUrl"""

    @patch("core_linked_records_app.components.data.api.get_pid_for_data")
    def test_get_pid_url_returns_pid_if_not_none(self, mock_get_pid_for_data):
        """test_get_pid_url_returns_pid_if_not_none

        Returns:

        """
        # Arrange
        mock_data = MagicMock()
        mock_data.id = 1
        mock_get_pid_for_data.return_value = (
            "http://localhost:8000/pid/rest/local/cdcs/test"
        )

        # Act + Assert
        self.assertIsNotNone(get_pid_url(data=mock_data, request=None))

    @patch("core_linked_records_app.components.data.api.get_pid_for_data")
    def test_get_pid_url_returns_none_if_none(self, mock_get_pid_for_data):
        """test_get_pid_url_returns_none_if_none

        Returns:

        """
        # Arrange
        mock_data = MagicMock()
        mock_data.id = 1
        mock_get_pid_for_data.return_value = None

        # Act + Assert
        self.assertIsNone(get_pid_url(data=mock_data, request=None))

    @patch("core_linked_records_app.components.data.api.get_pid_for_data")
    def test_get_pid_url_returns_none_if_api_error(
        self, mock_get_pid_for_data
    ):
        """test_get_pid_url_returns_none_if_api_error

        Returns:

        """
        # Arrange
        mock_data = MagicMock()
        mock_data.id = 1
        mock_get_pid_for_data.side_effect = ApiError("error")

        # Act + Assert
        self.assertIsNone(get_pid_url(data=mock_data, request=None))
