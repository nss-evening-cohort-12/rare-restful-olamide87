from django.db import models
from django.db.models import CASCADE

class Categories(models.Model):
    label = models.CharField(max_length=75)
    def __str__(self):
        return self.label
