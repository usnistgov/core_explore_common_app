""" Unit test views
"""
from unittest.mock import patch, MagicMock

from django.core.paginator import EmptyPage
from django.test import RequestFactory, SimpleTestCase

from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_explore_common_app.settings import SERVER_URI
from core_explore_common_app.views.user.ajax import (
    get_local_data_source,
    get_data_source_results,
    update_local_data_source,
)
from core_explore_common_app.views.user.views import ResultQueryRedirectView
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestGetLocalDataSource(SimpleTestCase):
    """TestGetLocalDataSource"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @patch("core_explore_common_app.utils.query.query.is_local_data_source")
    @patch(
        "core_explore_common_app.components.query.api.add_local_data_source"
    )
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_get_local_data_source(
        self,
        mock_get_by_id,
        mock_add_local_data_source,
        mock_is_local_data_source,
    ):
        """test_get_local_data_source

        Returns:

        """
        request = self.factory.get("core_explore_common_get_local_data_source")
        request.user = self.user1
        request.GET = {"query_id": "1"}

        mock_query = MagicMock()
        mock_query.data_sources = [
            {"name": "test", "url_query": "http://localhost:8000"}
        ]
        mock_get_by_id.return_value = mock_query
        mock_add_local_data_source.return_value = None
        mock_is_local_data_source.return_value = True

        response = get_local_data_source(request)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(mock_get_by_id.called)
        self.assertTrue(mock_add_local_data_source.called)
        self.assertTrue(mock_is_local_data_source.called)


class TestUpdateLocalDataSource(SimpleTestCase):
    """TestUpdateLocalDataSource"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @patch(
        "core_explore_common_app.components.query.api.add_local_data_source"
    )
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_update_local_data_source_selected(
        self, mock_get_by_id, mock_add_local_data_source
    ):
        """test_update_local_data_source_selected

        Returns:

        """
        request = self.factory.get(
            "core_explore_common_get_local_data_source",
            data={"query_id": "1", "selected": "true"},
        )
        request.user = self.user1

        mock_query = MagicMock()
        mock_query.content = {}

        mock_data_source = {
            "name": LOCAL_QUERY_NAME,
            "query_options": {},
            "order_by_field": [],
            "authentication": {"auth_type": "session"},
        }

        mock_query.data_sources = [mock_data_source]

        mock_get_by_id.return_value = mock_query
        mock_add_local_data_source.return_value = None

        response = update_local_data_source(request)

        self.assertTrue(response.status_code == 200)
        # Check add local data source called when selected
        self.assertTrue(mock_add_local_data_source.called)


class TestGetDataSourceResults(SimpleTestCase):
    """TestGetDataSourceResults"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @patch("core_explore_common_app.rest.query.views.format_local_results")
    @patch("core_explore_common_app.rest.query.views.execute_local_query")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_get_local_data_source_results(
        self,
        mock_get_by_id,
        mock_execute_local_query,
        mock_format_local_results,
    ):
        """test_get_local_data_source_results

        Returns:

        """
        request = self.factory.get("core_explore_common_get_local_data_source")
        request.user = self.user1

        mock_query = MagicMock()
        mock_query.content = {}

        mock_data_source = {
            "name": LOCAL_QUERY_NAME,
            "url_query": SERVER_URI,
            "query_options": {},
            "order_by_field": [],
            "authentication": {"auth_type": "session"},
        }

        mock_query.data_sources = [mock_data_source]

        mock_get_by_id.return_value = mock_query

        mock_results = MagicMock()
        mock_results.paginator.count = 1
        mock_results.previous_page_number.return_value = None
        mock_results.next_page_number.return_value = None
        mock_results.has_other_pages.return_value = False
        mock_results.has_previous.return_value = False
        mock_results.has_next.return_value = False
        mock_execute_local_query.return_value = mock_results
        mock_format_local_results.return_value = []

        response = get_data_source_results(
            request, query_id=1, data_source_index=0
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(mock_get_by_id.called)
        self.assertTrue(mock_execute_local_query.called)
        self.assertTrue(mock_format_local_results.called)

    @patch("core_explore_oaipmh_app.rest.query.views.format_oaipmh_results")
    @patch("core_explore_oaipmh_app.rest.query.views.execute_oaipmh_query")
    @patch("core_explore_common_app.utils.oaipmh.oaipmh.is_oai_data_source")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_get_oai_data_source_results(
        self,
        mock_get_by_id,
        mock_is_oai_data_source,
        mock_execute_oaipmh_query,
        mock_format_oaipmh_results,
    ):
        """test_get_oai_data_source_results

        Returns:

        """
        request = self.factory.get("core_explore_common_get_local_data_source")
        request.user = self.user1

        mock_query = MagicMock()
        mock_query.content = {}

        mock_data_source = {
            "name": "OAI-Server",
            "url_query": "http://localhost:8000",
            "query_options": {},
            "order_by_field": [],
            "authentication": {"auth_type": "session"},
        }

        mock_query.data_sources = [mock_data_source]

        mock_get_by_id.return_value = mock_query
        mock_is_oai_data_source.return_value = True

        mock_results = MagicMock()
        mock_results.paginator.count = 1
        mock_results.previous_page_number.return_value = None
        mock_results.next_page_number.return_value = None
        mock_results.has_other_pages.return_value = False
        mock_results.has_previous.return_value = False
        mock_results.has_next.return_value = False
        mock_execute_oaipmh_query.return_value = mock_results
        mock_format_oaipmh_results.return_value = []

        response = get_data_source_results(
            request, query_id=1, data_source_index=0
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(mock_get_by_id.called)
        self.assertTrue(mock_execute_oaipmh_query.called)
        self.assertTrue(mock_format_oaipmh_results.called)

    @patch("core_explore_common_app.utils.oaipmh.oaipmh.is_oai_data_source")
    @patch("core_explore_common_app.utils.query.query.is_local_data_source")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_get_unknown_data_source_results(
        self,
        mock_get_by_id,
        mock_is_local_data_source,
        mock_is_oai_data_source,
    ):
        """test_get_local_data_source_results

        Returns:

        """
        request = self.factory.get("core_explore_common_get_local_data_source")
        request.user = self.user1

        mock_query = MagicMock()
        mock_query.content = {}

        mock_data_source = {
            "name": "unknown",
            "url_query": "unknown",
            "query_options": {},
            "order_by_field": [],
            "authentication": {"auth_type": "session"},
        }

        mock_query.data_sources = [mock_data_source]

        mock_get_by_id.return_value = mock_query

        mock_is_local_data_source.return_value = False
        mock_is_oai_data_source.return_value = False

        response = get_data_source_results(
            request, query_id=1, data_source_index=0
        )
        self.assertTrue(response.status_code == 400)
        self.assertTrue(mock_get_by_id.called)
        self.assertTrue(mock_is_local_data_source.called)
        self.assertTrue(mock_is_oai_data_source.called)

    @patch("core_explore_common_app.rest.query.views.format_local_results")
    @patch("core_explore_common_app.rest.query.views.execute_local_query")
    @patch("core_explore_common_app.components.query.api.get_by_id")
    def test_get_local_data_source_results_no_next_previous_pages(
        self,
        mock_get_by_id,
        mock_execute_local_query,
        mock_format_local_results,
    ):
        """test_get_local_data_source_results_no_next_previous_pages

        Returns:

        """
        request = self.factory.get("core_explore_common_get_local_data_source")
        request.user = self.user1

        mock_query = MagicMock()
        mock_query.content = {}

        mock_data_source = {
            "name": LOCAL_QUERY_NAME,
            "url_query": SERVER_URI,
            "query_options": {},
            "order_by_field": [],
            "authentication": {"auth_type": "session"},
        }

        mock_query.data_sources = [mock_data_source]

        mock_get_by_id.return_value = mock_query

        mock_results = MagicMock()
        mock_results.paginator.count = 1
        mock_results.previous_page_number.side_effect = EmptyPage()
        mock_results.next_page_number.side_effect = EmptyPage()
        mock_results.has_other_pages.return_value = False
        mock_results.has_previous.return_value = False
        mock_results.has_next.return_value = False
        mock_execute_local_query.return_value = mock_results
        mock_format_local_results.return_value = []

        response = get_data_source_results(
            request, query_id=1, data_source_index=0
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(mock_get_by_id.called)
        self.assertTrue(mock_results.previous_page_number.called)
        self.assertTrue(mock_results.next_page_number.called)

    @patch("core_explore_common_app.components.query.api.get_by_id")
    @patch("core_explore_common_app.utils.query.query.send")
    def test_get_oauth2_data_source_results(
        self,
        mock_send_query,
        mock_get_by_id,
    ):
        """test_get_oauth2_data_source_results

        Returns:

        """
        request = self.factory.get("core_explore_common_get_local_data_source")
        request.user = self.user1

        mock_query = MagicMock()
        mock_query.content = {}

        mock_data_source = {
            "name": LOCAL_QUERY_NAME,
            "url_query": SERVER_URI,
            "query_options": {},
            "order_by_field": [],
            "authentication": {"auth_type": "oauth2"},
        }

        mock_query.data_sources = [mock_data_source]
        mock_get_by_id.return_value = mock_query
        mock_send_query.return_value = {
            "results": [],
            "previous": None,
            "next": None,
            "count": 1,
        }

        response = get_data_source_results(
            request, query_id=1, data_source_index=0
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(mock_get_by_id.called)
        self.assertTrue(mock_send_query.called)


class TestResultQueryRedirectView(SimpleTestCase):
    """TestResultQueryRedirectView"""

    @patch("core_explore_common_app.components.query.api.upsert")
    @patch(
        "core_explore_common_app.components.query.api.add_local_data_source"
    )
    def test_get_redirect_url(
        self, mock_add_local_data_source, mock_query_upsert
    ):
        """test_get_redirect_url

        Returns:

        """
        # Arrange
        mock_add_local_data_source.return_value = None
        mock_query = MagicMock()
        mock_templates_set = MagicMock()
        mock_templates = MagicMock()
        mock_templates.set.return_value = mock_templates_set
        mock_query.templates = mock_templates
        mock_query_upsert.return_value = mock_query

        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        mock_request.GET = {"id": "1"}
        view = TestRQRView()
        view.request = mock_request

        # Act
        url = view.get_redirect_url()

        # Assert
        self.assertTrue(mock_add_local_data_source.called)
        self.assertTrue(url, "url")


class TestRQRView(ResultQueryRedirectView):
    """TestRQRView"""

    @staticmethod
    def _get_persistent_query_by_id(persistent_query_id, user):
        persistent_query = MagicMock()
        persistent_query.content = {}
        persistent_query.data_sources = []
        return persistent_query

    @staticmethod
    def _get_persistent_query_by_name(persistent_query_name, user):
        pass

    @staticmethod
    def get_url_path():
        pass

    @staticmethod
    def _get_reversed_url(query):
        return "url"

    @staticmethod
    def _get_reversed_url_if_failed():
        pass
