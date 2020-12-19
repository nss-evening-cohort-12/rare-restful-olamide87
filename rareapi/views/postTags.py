"""View module for handling requests about postTags"""
from rareapi.models.postTags import PostTags
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Posts, Tags, PostTags

class PostTagsViewset(ViewSet):
  """rareapi postTags"""

  def create(self, request):
        """Handle POST operations"""

        post = Posts.objects.get(pk=request.data["posts"])
        tag = Tags.objects.get(pk=request.data["tags"])

        posttag = PostTags()
        posttag.posts = post
        posttag.tags = tag

        try: 
            posttag.save()
            serializer = PostTagsSerializer(posttag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



  def retrieve(self, request, pk=None):
        """Handle GET requests for single postTag

        Returns:
            Response -- JSON serialized postTag
        """
        try:
            posttags = PostTags.objects.get(pk=pk)
            serializer = PostTagsSerializer(posttags, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

  def list(self, request):
        """Handle GET requests to get all postTags

        Returns:
            Response -- JSON serialized list of postTags
        """
        posttags = PostTags.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostTagsSerializer(
            posttags, many=True, context={'request': request})
        return Response(serializer.data)

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tags
        fields = ('id', 'label')       


class PostTagsSerializer(serializers.ModelSerializer):
    """JSON serializer for postTags

    Arguments:
        serializers
    """
    tags = TagSerializer(many=False)

    class Meta:
        model = PostTags
        fields = ('tags', 'posts')
        depth = 1

