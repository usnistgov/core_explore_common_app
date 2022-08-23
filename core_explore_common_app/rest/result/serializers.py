"""Result serializers
"""
from rest_framework.serializers import ModelSerializer

from core_explore_common_app.components.result.models import Result


class ResultSerializer(ModelSerializer):
    """Result serializer"""

    class Meta:
        """Meta"""

        model = Result
        fields = "__all__"


class ResultBaseSerializer(ModelSerializer):
    """Result Serializer"""

    class Meta:
        """Meta"""

        model = Result
        fields = ("title", "xml_content")
