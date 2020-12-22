"""View module for handling requests about comments"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Posts, Comments

class CommentsViewset(ViewSet):
    """rare restful Comments"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment
        """
        try:
            comments = Comments.objects.get(pk=pk)
            serializer = CommentsSerializer(comments, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comments.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CommentsSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentsSerializer(serializers.ModelSerializer):
    """JSON serializer for comments

    Arguments:
        serializers
    """
    class Meta:
        model = Comments
        fields = ('posts', 'subject','created_on', 'content')


        


