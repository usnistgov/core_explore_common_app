"""
Query models
"""

from mongoengine import errors as mongoengine_errors

from core_explore_common_app.components.abstract_query.models import AbstractQuery
from core_main_app.commons import exceptions


# TODO: remove old queries from database


class Query(AbstractQuery):
    """Query class"""

    @staticmethod
    def get_by_id(query_id):
        """Returns a query given its id

        Args:
            query_id:

        Returns:

        """
        try:
            return Query.objects.get(pk=str(query_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def get_data_source_by_name_and_url_query(self, name, url_query):
        """Returns a data source from given name and url of query

        Args:
            name:
            url_query:

        Returns:

        """
        for data_source in self.data_sources:
            if data_source.name == name and data_source.url_query == url_query:
                return data_source
        raise exceptions.DoesNotExist(
            "No data source found fot the given name and url."
        )
