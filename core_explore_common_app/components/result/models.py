"""Result models
"""
from django_mongoengine import fields, Document, EmbeddedDocument


class TemplateInfo(EmbeddedDocument):
    """Template information class
    """
    id = fields.StringField(blank=True)
    name = fields.StringField(blank=False)
    hash = fields.StringField(blank=False)


class Result(Document):
    """Result class
    """
    title = fields.StringField(blank=False)
    xml_content = fields.StringField(blank=False)
    template_info = fields.EmbeddedDocumentField(TemplateInfo)
    detail_url = fields.StringField(blank=True)
    access_data_url = fields.StringField(blank=True)
