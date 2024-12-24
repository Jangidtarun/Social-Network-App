from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    content = models.CharField(max_length=240)
    timestamp = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='liked')

    def __str__(self):
        return f"{self.id}: {self.poster} posted {self.content}"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followeruser')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followinguser')

    def __str__(self) -> str:
        return f"{self.follower} following {self.following}"