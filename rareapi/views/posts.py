"""View module for handling requests about game types"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Posts

class PostsViewset(ViewSet):
    """Level up posts"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Posts.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all Posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Posts.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializers
    """
    class Meta:
        model = Posts
        # url = serializers.HyperlinkedIdentityField(
        #     view_name='posts',
        #     lookup_field='id',



        # )
        fields = ('id', 'title', 'publication_date', 
        'image_url','content', 'approved' )
