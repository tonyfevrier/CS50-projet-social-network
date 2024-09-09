from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from project4 import settings

class User(AbstractUser):
    following = models.JSONField(default=[])


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post")
    text = models.TextField(default="")
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)