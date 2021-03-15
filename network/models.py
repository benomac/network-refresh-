from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(default=0)
    followed = models.IntegerField(default=0)
    def serialize(self):
        return {
            "followers": self.followers,
            "followed": self.followed
            

        }
  

class UserPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    post = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "Post": self.post,
            "Posted": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "user": self.user.username

        }
  

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")

    def serialize(self):
        return {
            "user": self.user,
            "following": self.following,
            

        }