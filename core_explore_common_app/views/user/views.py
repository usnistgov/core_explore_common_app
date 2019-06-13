""" Explore Common Views
"""
from abc import ABCMeta, abstractmethod

from django.contrib import messages
from django.views.generic import RedirectView

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query


class ResultQueryRedirectView(RedirectView, metaclass=ABCMeta):
    def get_redirect_url(self, *args, **kwargs):
        try:
            # here we receive a PersistentQuery id
            persistent_query_example = self._get_persistent_query(kwargs['persistent_query_id'])

            # from it we have to duplicate it to a Query with the new user_id
            # we should probably add the query_id into the persistent query?
            # to avoid to recreate this query each time we visit the persistent URL
            query = Query(user_id=str(self.request.user.id),
                          content=persistent_query_example.content,
                          templates=persistent_query_example.templates,
                          data_sources=persistent_query_example.data_sources)
            query = query_api.upsert(query)

            # then redirect to the result page core_explore_example_results with /<template_id>/<query_id>
            return self._get_reversed_url(query)
        except Exception as e:
            # add success message
            messages.add_message(self.request, messages.ERROR, 'The given URL is not valid.')
            return self._get_reversed_url_if_failed()

    @staticmethod
    @abstractmethod
    def _get_persistent_query(persistent_query_id):
        raise NotImplementedError("_get_persistent_query method is not implemented.")

    @staticmethod
    @abstractmethod
    def _get_reversed_url(query):
        raise NotImplementedError("_get_reversed_url method is not implemented.")

    @staticmethod
    @abstractmethod
    def _get_reversed_url_if_failed():
        raise NotImplementedError("_get_reversed_url_if_failed method is not implemented.")

