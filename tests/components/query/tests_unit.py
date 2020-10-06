""" Unit Test Query
"""
from unittest.case import TestCase

from mock import patch

from core_explore_common_app.components.abstract_query.models import (
    Authentication,
    DataSource,
)
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestQueryUpsert(TestCase):
    @patch.object(Query, "save")
    def test_upsert_query_returns_query(self, mock_save):
        query = _create_query()
        mock_save.return_value = query
        mock_user = create_mock_user("1")
        self.assertTrue(isinstance(query_api.upsert(query, mock_user), Query))


class TestQueryGetById(TestCase):
    @patch.object(Query, "get_by_id")
    def test_saved_query_get_by_id_raises_api_error_if_not_found(self, mock_get):
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_user = create_mock_user("1")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            query_api.get_by_id("1", mock_user)

    @patch.object(Query, "get_by_id")
    def test_query_get_by_id_return_data_if_found(self, mock_get):
        # Arrange
        query = _create_query()
        mock_get.return_value = query
        mock_user = create_mock_user("1")
        # Act
        result = query_api.get_by_id(query.id, mock_user)
        # Assert
        self.assertIsInstance(result, Query)


class TestGetDataSourceByNameAndUrlQuery(TestCase):
    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_saved_query_get_by_name_and_url_raises_api_error_if_not_found(
        self, mock_get
    ):
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
    @patch.object(Query, "save")
    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_add_data_source_adds_data_source_if_not_found(self, mock_get, mock_save):
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

    @patch.object(Query, "save")
    @patch.object(Query, "get_data_source_by_name_and_url_query")
    def test_add_data_source_does_not_add_data_source_if_found(
        self, mock_get, mock_save
    ):
        # create query
        query = _create_query()
        # Arrange
        mock_get.return_value = query.data_sources[0]
        mock_save.return_value = query
        mock_user = create_mock_user("1")

        origin_data_sources = len(query.data_sources)
        data_source = _create_data_source("Remote", "/remote/url")
        query_api.add_data_source(query, data_source, mock_user)
        self.assertTrue(len(query.data_sources) == origin_data_sources)


class TestQueryRemoveDataSource(TestCase):
    @patch.object(Query, "save")
    def test_remove_data_source(self, mock_save):
        # create query
        query = _create_query()
        mock_save.return_value = query
        mock_user = create_mock_user("1")
        origin_data_sources = len(query.data_sources)
        data_source = query.data_sources[0]
        query_api.remove_data_source(query, data_source, mock_user)
        self.assertTrue(len(query.data_sources) == origin_data_sources - 1)


def _create_data_source(name="Local", url="/url"):
    authentication = Authentication(type="session")
    data_source = DataSource(name=name, url_query=url, authentication=authentication)
    return data_source


def _create_query():
    data_source = _create_data_source()
    query = Query(
        user_id="1",
        content="{'root.value': 'test'}",
        templates=[],
        data_sources=[data_source],
    )
    return query
