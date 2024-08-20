""" Unit tests for `core_explore_common_app.utils.protocols.oauth2` package.
"""

from unittest import TestCase
from unittest.mock import patch

from core_explore_common_app.utils.protocols import oauth2 as oauth2_protocol


class TestSendGetRequest(TestCase):
    """Unit tests for `send_get_request` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"url": "mock_url"}

    @patch.object(oauth2_protocol, "requests_utils")
    def test_no_access_token_sends_request_without_auth_header(
        self, mock_requests_utils
    ):
        """test_no_access_token_sends_request_without_auth_header"""
        self.mock_kwargs["access_token"] = None
        oauth2_protocol.send_get_request(**self.mock_kwargs)

        mock_requests_utils.send_get_request.assert_called_with(
            self.mock_kwargs["url"], headers={}
        )

    @patch.object(oauth2_protocol, "requests_utils")
    def test_access_token_sends_request_with_auth_header(
        self, mock_requests_utils
    ):
        """test_access_token_sends_request_with_auth_header"""
        self.mock_kwargs["access_token"] = "mock_access_token"
        oauth2_protocol.send_get_request(**self.mock_kwargs)

        mock_requests_utils.send_get_request.assert_called_with(
            self.mock_kwargs["url"],
            headers={
                "Authorization": f"Bearer {self.mock_kwargs['access_token']}"
            },
        )


class TestSendPostRequest(TestCase):
    """Unit tests for `send_post_request` function."""

    def setUp(self):
        """setUp"""
        self.tz = "mock_tz"
        self.mock_kwargs = {
            "url": "mock_url",
            "session_time_zone": self.tz,
            "data": "mock_data",
        }
        self.headers = {"TZ": self.tz}

    @patch.object(oauth2_protocol, "requests_utils")
    def test_no_access_token_sends_request_without_auth_header(
        self, mock_requests_utils
    ):
        """test_no_access_token_sends_request_without_auth_header"""
        self.mock_kwargs["access_token"] = None
        oauth2_protocol.send_post_request(**self.mock_kwargs)

        mock_requests_utils.send_post_request.assert_called_with(
            self.mock_kwargs["url"],
            data=self.mock_kwargs["data"],
            headers=self.headers,
        )

    @patch.object(oauth2_protocol, "requests_utils")
    def test_access_token_sends_request_with_auth_header(
        self, mock_requests_utils
    ):
        """test_access_token_sends_request_with_auth_header"""
        self.mock_kwargs["access_token"] = "mock_access_token"
        oauth2_protocol.send_post_request(**self.mock_kwargs)

        self.headers["Authorization"] = (
            f"Bearer {self.mock_kwargs['access_token']}"
        )

        mock_requests_utils.send_post_request.assert_called_with(
            self.mock_kwargs["url"],
            data=self.mock_kwargs["data"],
            headers=self.headers,
        )
