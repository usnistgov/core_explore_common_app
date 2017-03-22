"""
Query models
"""
from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template


# TODO: remove old queries from database

AUTH_TYPES = ('session', 'oauth2')


class Authentication(EmbeddedDocument):
    """Authentication class
    """
    type = fields.StringField(choices=AUTH_TYPES)
    params = fields.DictField(blank=True)


class DataSource(EmbeddedDocument):
    """Data Source class
    """
    name = fields.StringField(blank=False)
    url_query = fields.StringField(blank=False)
    query_options = fields.DictField(blank=True)
    authentication = fields.EmbeddedDocumentField(Authentication)


class Query(Document):
    """Query class
    """
    user_id = fields.StringField(blank=False)
    content = fields.StringField(blank=True)
    templates = fields.ListField(fields.ReferenceField(Template, blank=True), blank=True, default=[])
    data_sources = fields.ListField(fields.EmbeddedDocumentField(DataSource, blank=True), blank=True, default=[])

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
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

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
        raise exceptions.DoesNotExist("No data source found fot the given name and url.")
