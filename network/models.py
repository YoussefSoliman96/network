from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    content = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default = '0')
    
    def __str__(self):
        return f"{self.id} by {self.user} on {self.created_at} has {self.likes} likes"
    
class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    def __str__(self):
        return f"{self.following} is following {self.followed}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Like_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.user} liked {self.post}"
    
class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentWriter")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="postComments")
    comment = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.writer} commented on {self.post}"
