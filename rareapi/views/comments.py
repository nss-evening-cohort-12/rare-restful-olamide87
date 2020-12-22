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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized comments instance
        """

        # # Uses the token passed in the `Authorization` header
        # categories = Categories.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        comment = Comments()
        comment.subject = request.data["subject"]
        comment.created_on = request.data["created_on"]
        comment.content = request.data["content"]
        comment.posts = Posts.objects.get(pk=request.data["posts"])

        # Use the Django ORM to get the record from the database
        # # whose `id` is what the client passed as the
        # # `gameTypeId` in the body of the request.
        # category = Categories.objects.get(pk=request.data["categoryId"])
        # category.categories = category

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            comment.save()
            serializer = CommentsSerializer(comment, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for an comments

        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comments.objects.get(pk=pk)
        comment.subject = request.data["subject"]
        comment.created_on = request.data["created_on"]
        comment.content = request.data["content"]
        comment.posts = Posts.objects.get(pk=request.data["posts"])

        # game = Game.objects.get(pk=request.data["gameId"])
        # event.game = game
        comment.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
                    

class CommentsSerializer(serializers.ModelSerializer):
    """JSON serializer for comments

    Arguments:
        serializers
    """
    class Meta:
        model = Comments
        fields = ('posts', 'subject','created_on', 'content')


        


