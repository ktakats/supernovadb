from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Comment(models.Model):

    text=models.CharField(max_length=200)
    pub_date=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
