""" Authentication tests for Local Query REST API
"""
from django.test import SimpleTestCase
from mock import patch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_explore_common_app.rest.query import views as explore_rest_views
from core_explore_common_app.rest.query.views import AbstractExecuteLocalQueryView


class TestExecuteLocalQueryViewGetPermissions(SimpleTestCase):
    """Test Execute Local Query View Get Permissions"""

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200

        Returns:

        """
        mock_execute_query.return_value = Response(status=HTTP_200_OK)

        response = RequestMock.do_request_get(
            explore_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200

        Returns:

        """
        mock_execute_query.return_value = Response(status=HTTP_200_OK)

        response = RequestMock.do_request_get(
            explore_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200

        Returns:

        """
        mock_execute_query.return_value = Response(status=HTTP_200_OK)

        response = RequestMock.do_request_get(
            explore_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestExecuteLocalQueryViewPostPermissions(SimpleTestCase):
    """Test Execute Local Query View Post Permissions"""

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200

        Returns:

        """
        mock_execute_query.return_value = Response(status=HTTP_200_OK)

        response = RequestMock.do_request_post(
            explore_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200

        Returns:

        """
        mock_execute_query.return_value = Response(status=HTTP_200_OK)

        response = RequestMock.do_request_post(
            explore_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200

        Returns:

        """
        mock_execute_query.return_value = Response(status=HTTP_200_OK)

        response = RequestMock.do_request_post(
            explore_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
