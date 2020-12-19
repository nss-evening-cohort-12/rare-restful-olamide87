""" PostTag model module """

from django.db import models

class PostTags(models.Model):
    """PostTag database model"""
    
    tags = models.ForeignKey("Tags", on_delete=models.CASCADE, related_name="tagging" )
    posts = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="tagging" )
