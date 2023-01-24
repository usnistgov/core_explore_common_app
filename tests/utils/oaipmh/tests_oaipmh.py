""" OAI-PMH utils test class
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.test import override_settings

from core_explore_common_app.utils.oaipmh.oaipmh import is_oai_data_source


class TestIsOaiDataSource(TestCase):
    """TestIsOaiDataSource"""

    @patch("core_oaipmh_harvester_app.components.oai_registry.api.get_all")
    def test_is_oai_data_source_returns_true_if_oai_data_source(
        self, mock_get_all
    ):
        """test_is_oai_data_source_returns_true_if_oai_data_source

        Returns:

        """
        # Arrange
        mock_data_source = {"name": "oaipmh"}
        oai_get_all_response = MagicMock()
        oai_get_all_response.values_list.return_value = ["oaipmh"]
        mock_get_all.return_value = oai_get_all_response

        # Act + Assert
        self.assertTrue(is_oai_data_source(mock_data_source))

    @patch("core_oaipmh_harvester_app.components.oai_registry.api.get_all")
    def test_is_oai_data_source_returns_false_if_not_oai_data_source(
        self, mock_get_all
    ):
        """test_is_oai_data_source_returns_false_if_not_oai_data_source

        Returns:

        """
        # Arrange
        mock_data_source = {"name": "oaipmh"}
        oai_get_all_response = MagicMock()
        oai_get_all_response.values_list.return_value = ["not-oaipmh"]
        mock_get_all.return_value = oai_get_all_response

        # Act + Assert
        self.assertFalse(is_oai_data_source(mock_data_source))

    @override_settings(INSTALLED_APPS=[])
    def test_is_oai_data_source_returns_false_if_oai_not_installed(self):
        """test_is_oai_data_source_returns_false_if_oai_not_installed

        Returns:

        """
        # Arrange
        mock_data_source = {"name": "oaipmh"}

        # Act + Assert
        self.assertFalse(is_oai_data_source(mock_data_source))
