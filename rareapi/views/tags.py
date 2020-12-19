"""View module for handling requests about tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tags


class TagsViewset(ViewSet):
    """rare restful Tags"""
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized category instance
        """

        # # Uses the token passed in the `Authorization` header
        # categories = Categories.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        tag = Tags()
        tag.label = request.data["label"]
       

        # Use the Django ORM to get the record from the database
        # # whose `id` is what the client passed as the
        # # `gameTypeId` in the body of the request.
        # category = Categories.objects.get(pk=request.data["categoryId"])
        # category.categories = category

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            tag.save()
            serializer = TagsSerializer(tag, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

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

    def update(self, request, pk=None):
        """Handle PUT requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """
        # gamer = Gamer.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        tag = Tags.objects.get(pk=pk)
        tag.label = request.data["label"]
      

        tag.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)        

    def list(self, request):
        """Handle GET requests to get all Tags

        Returns:
            Response -- JSON serialized list of Tags
        """
        tags = Tags.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TagsSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
        

class TagsSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializers
    """
    class Meta:
        model = Tags
        fields = ('id', 'label')

