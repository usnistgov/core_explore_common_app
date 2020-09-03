""" Abstract Query model
"""
from django_mongoengine import fields, Document
from mongoengine import EmbeddedDocument

from core_main_app.components.template.models import Template

AUTH_TYPES = ("session", "oauth2")


class Authentication(EmbeddedDocument):
    """Authentication class"""

    type = fields.StringField(choices=AUTH_TYPES)
    params = fields.DictField(blank=True)


class DataSource(EmbeddedDocument):
    """Data Source class"""

    name = fields.StringField(blank=False)
    url_query = fields.StringField(blank=False)
    query_options = fields.DictField(blank=True)
    authentication = fields.EmbeddedDocumentField(Authentication)
    order_by_field = fields.StringField(blank=True, default="")
    capabilities = fields.DictField(blank=True)


class AbstractQuery(Document):
    """Abstract Query"""

    user_id = fields.StringField(blank=False)
    content = fields.StringField(blank=True)
    templates = fields.ListField(
        fields.ReferenceField(Template, blank=True), blank=True, default=[]
    )
    data_sources = fields.ListField(
        fields.EmbeddedDocumentField(DataSource, blank=True), blank=True, default=[]
    )

    meta = {
        "abstract": True,
    }
