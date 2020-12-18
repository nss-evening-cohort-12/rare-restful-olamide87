"""View module for handling requests about game types"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Posts, Categories

class PostsViewset(ViewSet):
    """Level up posts"""

    def create(self, request):
        """Handle POST operations for events

        Returns:
            Response -- JSON serialized post instance
        """
        post = Posts()
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]
        post.content = request.data["content"]
        post.category = Categories.objects.get(pk=request.data["category_id"])
        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)    

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

    def update(self, request, pk=None):
        """Handle PUT requests for an post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Posts.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]
        post.content = request.data["content"]
        post.category = Categories.objects.get(pk=request.data["category_id"])
    

        # game = Game.objects.get(pk=request.data["gameId"])
        # event.game = game
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

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
        fields = ('id', 'title', 'publication_date', 
        'image_url','content', 'approved' )
