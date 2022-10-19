from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.CharField(max_length=200)
    content = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

class Like(models.Model):
    liker = models.CharField(max_length=200)
    post_id = models.CharField(max_length=200)

class Follow(models.Model):
    follower = models.CharField(max_length=200)
    creator = models.CharField(max_length=200)
