""" Authentication tests for Query Results REST API
"""
from collections import OrderedDict

from django.test import SimpleTestCase
from mock import patch
from rest_framework import status

import core_main_app.components.data.api as data_api
from core_explore_common_app.rest.result.views import get_result_from_data_id
from core_main_app.components.data.models import Data
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestResultFromDataIdGetPermissions(SimpleTestCase):
    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_200(self, mock_data_get_by_id):
        mock_data = Data(
            template="template", user_id="1", dict_content=OrderedDict(), title="title"
        )
        mock_data_get_by_id.return_value = mock_data

        response = RequestMock.do_request_get(
            get_result_from_data_id, None, data={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(self, mock_data_get_by_id):
        mock_data = Data(
            template="template", user_id="1", dict_content=OrderedDict(), title="title"
        )
        mock_data_get_by_id.return_value = mock_data
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            get_result_from_data_id, mock_user, data={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(self, mock_data_get_by_id):
        mock_data = Data(
            template="template", user_id="1", dict_content=OrderedDict(), title="title"
        )
        mock_data_get_by_id.return_value = mock_data
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            get_result_from_data_id, mock_user, data={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
