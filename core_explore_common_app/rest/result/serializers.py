"""Result serializers
"""

from rest_framework_mongoengine.serializers import DocumentSerializer
from core_explore_common_app.components.result.models import Result


class ResultSerializer(DocumentSerializer):
    """ Result serializer
    """
    class Meta:
        """ Meta
        """
        model = Result
        fields = "__all__"
