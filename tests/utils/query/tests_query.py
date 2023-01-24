""" Query utils test class
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_explore_common_app.commons.exceptions import ExploreRequestError
from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_explore_common_app.settings import SERVER_URI
from core_explore_common_app.utils.query import query
from core_explore_common_app.utils.query.query import is_local_data_source


class TestSendQuery(TestCase):
    """TestSendQuery"""

    @patch("core_explore_common_app.utils.protocols.oauth2.send_post_request")
    def test_send_oauth2_query(self, mock_oauth2_send_post_request):
        """test_send_oauth2_query

        Returns:

        """
        # Arrange
        mock_data_source = {
            "authentication": {
                "auth_type": "oauth2",
                "params": {"access_token": "token"},
            },
            "url_query": "http://localhost:8000",
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_oauth2_send_post_request.return_value = mock_response

        # Act
        response = query.send(
            request=None, json_query={}, data_source=mock_data_source, page=1
        )

        # Assert
        self.assertIsNotNone(response)

    def test_send_query_with_unknown_protocol_fails(self):
        # Arrange
        mock_data_source = {"authentication": {"auth_type": "test"}}

        # Act + Assert
        with self.assertRaises(ExploreRequestError):
            query.send(
                request=None,
                json_query={},
                data_source=mock_data_source,
                page=1,
            )


class TestIsLocalDataSource(TestCase):
    """TestIsLocalDataSource"""

    def test_is_local_data_source_with_local_params_returns_true(self):
        """test_is_local_data_source_with_local_params_returns_true

        Returns:

        """
        data_source = {"name": LOCAL_QUERY_NAME, "url_query": SERVER_URI}
        self.assertTrue(is_local_data_source(data_source))

    def test_is_local_data_source_with_wrong_name_returns_false(self):
        """test_is_local_data_source_with_wrong_name_returns_false

        Returns:

        """
        data_source = {"name": "bad", "url_query": SERVER_URI}
        self.assertFalse(is_local_data_source(data_source))

    def test_is_local_data_source_with_wrong_url_returns_false(self):
        """test_is_local_data_source_with_wrong_url_returns_false

        Returns:

        """
        data_source = {"name": LOCAL_QUERY_NAME, "url_query": "bad"}
        self.assertFalse(is_local_data_source(data_source))

    def test_is_local_data_source_with_wrong_params_returns_false(self):
        """test_is_local_data_source_with_wrong_params_returns_false

        Returns:

        """
        data_source = {"name": "bad", "url_query": "bad"}
        self.assertFalse(is_local_data_source(data_source))
