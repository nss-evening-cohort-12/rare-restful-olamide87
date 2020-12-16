from django.db import models
from django.db.models import CASCADE

class Posts(models.Model):
    category = models.ForeignKey("Categories",on_delete=CASCADE)
    title = models.CharField(max_length=75)
    publication_date = models.DateField()
    image_url =  models.CharField(max_length=75)
    content =  models.TextField()
    approved =  models.BooleanField()
