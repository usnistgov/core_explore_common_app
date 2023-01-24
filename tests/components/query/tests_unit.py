""" Unit Test Query
"""
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.test import override_settings

from core_explore_common_app.components.abstract_query.models import (
    Authentication,
    DataSource,
)
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_common_app.settings import QUERY_VISIBILITY, SERVER_URI
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestQueryUpsert(TestCase):
    """Test Query Upsert"""

    @patch.object(Query, "save")
    def test_upsert_query_returns_query(self, mock_save):
        """test_upsert_query_returns_query

        Returns:

        """
        query = _create_query()
        mock_save.return_value = query
        mock_user = create_mock_user("1")
        self.assertTrue(isinstance(query_api.upsert(query, mock_user), Query))


class TestQueryGetById(TestCase):
    """Test Query Get By Id"""

    @patch.object(Query, "get_by_id")
    def test_saved_query_get_by_id_raises_api_error_if_not_found(
        self, mock_get
    ):
        """test_saved_query_get_by_id_raises_api_error_if_not_found

        Returns:

        """
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_user = create_mock_user("1")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            query_api.get_by_id("1", mock_user)

    @patch.object(Query, "get_by_id")
    def test_query_get_by_id_return_data_if_found(self, mock_get):
        """test_query_get_by_id_return_data_if_found

        Returns:

        """
        # Arrange
        query = _create_query()
        mock_get.return_value = query
        mock_user = create_mock_user("1")
        # Act
        result = query_api.get_by_id(query.id, mock_user)
        # Assert
        self.assertIsInstance(result, Query)


class TestGetDataSourceByNameAndUrlQuery(TestCase):
    """Test Get Data Source By Name And Url Query"""

    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_saved_query_get_by_name_and_url_raises_api_error_if_not_found(
        self, mock_get
    ):
        """test_saved_query_get_by_name_and_url_raises_api_error_if_not_found

        Returns:

        """
        # create query
        query = _create_query()
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_user = create_mock_user("1")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            query_api.get_data_source_by_name_and_url_query(
                query, "name", "url", mock_user
            )

    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_query_get_by_id_return_data_if_found(self, mock_get):
        """test_query_get_by_id_return_data_if_found

        Returns:

        """
        # create query
        query = _create_query()
        # Arrange
        mock_get.return_value = query
        mock_user = create_mock_user("1")
        # Act
        result = query_api.get_data_source_by_name_and_url_query(
            query, "Data Source", "/url", mock_user
        )
        # Assert
        self.assertIsInstance(result, Query)


class TestQueryAddDataSource(TestCase):
    """Test Query Add Data Source"""

    @patch.object(Query, "save")
    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_add_data_source_adds_data_source_if_not_found(
        self, mock_get, mock_save
    ):
        """test_add_data_source_adds_data_source_if_not_found

        Returns:

        """
        # create query
        query = _create_query()
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_save.return_value = query
        mock_user = create_mock_user("1")

        origin_data_sources = len(query.data_sources)
        data_source = _create_data_source("Remote", "/remote/url")
        query_api.add_data_source(query, data_source, mock_user)
        self.assertTrue(len(query.data_sources) == origin_data_sources + 1)

    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_add_data_source_does_not_add_data_source_if_found(
        self,
        mock_get,
    ):
        """test_add_data_source_does_not_add_data_source_if_found

        Returns:

        """
        # create query
        query = _create_query()
        # Arrange
        data_source = _create_data_source("Remote", "/remote/url")
        query.data_sources = [data_source]
        mock_get.return_value = data_source

        mock_user = create_mock_user("1")

        result = query_api.add_data_source(query, data_source, mock_user)
        self.assertTrue(result.data_sources == query.data_sources)


class TestQueryRemoveDataSource(TestCase):
    """Test Query Remove Data Source"""

    @patch.object(Query, "save")
    def test_remove_data_source(self, mock_save):
        """test_remove_data_source

        Returns:

        """
        # create query
        query = _create_query()
        mock_save.return_value = query
        mock_user = create_mock_user("1")
        data_source = _create_data_source()
        query.data_sources = [data_source]
        origin_data_sources = len(query.data_sources)
        query_api.remove_data_source(query, data_source, mock_user)
        self.assertTrue(len(query.data_sources) == origin_data_sources - 1)


class TestSetVisibilityToQuery(TestCase):
    """Test Set Visibility To Query"""

    def test_set_visibility_to_query_changes_visibility_to_public(self):
        """test_set_visibility_to_query_changes_visibility_to_public

        Returns:

        """
        # create query
        query = _create_query()
        query.data_sources = [_create_data_source()]

        mock_user = create_mock_user("1")

        query_api.set_visibility_to_query(query, mock_user)

        for data_source in query.data_sources:
            self.assertTrue(
                data_source["query_options"]["visibility"], QUERY_VISIBILITY
            )


class TestAddLocalDataSource(TestCase):
    """TestAddLocalDataSource"""

    @override_settings(INSTALLED_APPS=[])
    @patch(
        "core_explore_common_app.utils.query.query.create_local_data_source"
    )
    @patch("core_explore_common_app.components.query.api.add_data_source")
    def test_add_local_data_source(
        self, mock_create_local_data_source, mock_add_data_source
    ):
        """test_upsert_query_returns_query

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_request = create_mock_request(mock_user)

        mock_data_source = MagicMock()
        mock_create_local_data_source.return_value = mock_data_source
        mock_add_data_source.return_value = None
        query_api.add_local_data_source(mock_request, mock_data_source)


def _create_data_source(name="Local", url=SERVER_URI):
    """_create_data_source

    Returns:
    """
    authentication = Authentication(auth_type="session")
    data_source = DataSource(
        name=name, url_query=url, authentication=authentication
    )
    return data_source


def _create_query():
    """_create_query

    Returns:
    """
    query = Query(
        id=1,
        user_id="1",
        content="{'root.value': 'test'}",
    )
    return query
