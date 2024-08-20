""" Unit tests of data_to_html templatetag
"""

from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from core_explore_common_app.components.result.models import Result
from core_main_app.commons.exceptions import DoesNotExist
from core_explore_common_app.templatetags.result_to_html import (
    result_list_html,
)


class TestResultToHtml(TestCase):
    """TestResultToHtml"""

    def test_result_html_with_none_returns_none(self):
        """test_result_html_with_none_returns_none

        Returns:

        """
        result = result_list_html(None)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_without_template_html_rendering_returns_none(
        self, mock_get_by_template_id
    ):
        """test_result_html_without_template_html_rendering_returns_none

        Returns:

        """
        mock_get_by_template_id.side_effect = DoesNotExist("Error")
        mock_data = {
            "content": {"value": "test"},
            "template_info": {"format": "JSON", "id": 1},
        }
        result = result_list_html(mock_data)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_without_detail_rendering_returns_none(
        self, mock_get_by_template_id
    ):
        """test_result_html_without_detail_rendering_returns_none

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = None
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_result = {
            "content": {"value": "test"},
            "template_info": {"format": "JSON", "id": 1},
        }
        result = result_list_html(mock_result)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_with_dict_returns_html(self, mock_get_by_template_id):
        """test_result_html_with_dict_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = "{{dict_content.value}}"
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_result = {
            "content": {"value": "test"},
            "template_info": {"format": "JSON", "id": 1},
        }
        result = result_list_html(mock_result)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_with_string_dict_returns_html(
        self, mock_get_by_template_id
    ):
        """test_result_html_with_dict_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = "{{dict_content.value}}"
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_result = {
            "content": '{"value": "test"}',
            "template_info": {"format": "JSON", "id": 1},
        }
        result = result_list_html(mock_result)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_returns_html(self, mock_get_by_template_id):
        """test_result_html_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = "{{dict_content.value}}"
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_result = Result(
            content={"value": "test"},
            template_info={"format": "JSON", "id": 1},
        )
        result = result_list_html(mock_result)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_with_xml_returns_html(self, mock_get_by_template_id):
        """test_result_html_with_xml_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = "{{dict_content.value}}"
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_result = {
            "content": "<value>test</value>",
            "template_info": {"format": "XSD", "id": 1},
        }
        result = result_list_html(mock_result)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_result_html_with_unknown_format_returns_none(
        self, mock_get_by_template_id
    ):
        """test_result_html_with_unknown_format_returns_none

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = "{{dict_content.value}}"
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_result = {
            "content": "value: test",
            "template_info": {"format": "YAML", "id": 1},
        }
        result = result_list_html(mock_result)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_hash"
    )
    def test_result_html_get_by_hash_with_dict_returns_html(
        self, mock_get_by_template_hash
    ):
        """test_result_html_get_by_hash_with_dict_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.list_rendering = "{{dict_content.value}}"
        mock_get_by_template_hash.return_value = mock_template_html_rendering
        mock_result = {
            "content": {"value": "test"},
            "template_info": {"format": "JSON", "hash": "abcd"},
        }
        result = result_list_html(mock_result)
        self.assertEqual(result, "test")

    def test_result_html_returns_none_if_id_or_hash_missing(
        self,
    ):
        """test_result_html_returns_none_if_id_or_hash_missing

        Returns:

        """
        mock_result = {
            "content": {"value": "test"},
            "template_info": {"format": "JSON"},
        }
        result = result_list_html(mock_result)
        self.assertIsNone(result)

    def test_result_html_returns_none_if_template_info_missing(
        self,
    ):
        """test_result_html_returns_none_if_template_info_missing

        Returns:

        """
        mock_result = {
            "content": {"value": "test"},
        }
        result = result_list_html(mock_result)
        self.assertIsNone(result)
