"""Result models
"""
from django_mongoengine import fields, Document


class Result(Document):
    """Result class
    """
    title = fields.StringField(blank=False)
    xml_content = fields.StringField(blank=False)
    origin = fields.StringField(blank=True)
    detail_url = fields.StringField(blank=True)
