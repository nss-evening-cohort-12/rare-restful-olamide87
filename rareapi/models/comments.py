from django.db import models
from django.db.models import CASCADE


class Comments(models.Model):
   posts = models.ForeignKey("Posts", on_delete=models.CASCADE)
   created_on = models.DateField()
   subject = models.CharField(max_length=75)
   content =  models.TextField()


  
