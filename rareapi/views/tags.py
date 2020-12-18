"""View module for handling requests about tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tags


class TagsViewset(ViewSet):
    """rare restful Tags"""


    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized category
        """
        try:
            tags = Tags.objects.get(pk=pk)
            serializer = TagsSerializer(tags, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class TagsSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializers
    """
    class Meta:
        model = Tags
        fields = ('id', 'label')

