from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from project4 import settings
import json

class User(AbstractUser):
    following = models.JSONField(default=[])
    followers = models.JSONField(default=[])

    def serialize(self):
        return {'username':self.username,
                'following_number':len(self.following),
                'followers_number':len(self.followers)}


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post")
    text = models.TextField(default="")
    date = models.DateTimeField(default=timezone.now)
    likes = models.JSONField(default=[])

    def serialize(self):
        return {'id': self.id,
                'username':self.user.username,
                'text':self.text,
                'date':self.date.strftime("%b %d %Y, %I:%M %p"),
                'likes':len(self.likes)}