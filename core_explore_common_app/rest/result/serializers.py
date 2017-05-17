"""Result serializers
"""
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from core_explore_common_app.components.result.models import Result, TemplateInfo


class TemplateInfoSerializer(EmbeddedDocumentSerializer):
    """ Template info serializer
    """
    class Meta:
        """ Meta
        """
        model = TemplateInfo
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'allow_blank': True,
            }
        }


class ResultSerializer(DocumentSerializer):
    """ Result serializer
    """
    template_info = TemplateInfoSerializer(many=False)

    class Meta:
        """ Meta
        """
        model = Result
        fields = "__all__"


class ResultBaseSerializer(DocumentSerializer):
    """ Result Serializer
    """

    class Meta:
        """ Meta
        """
        model = Result
        fields = ('title', 'xml_content')
