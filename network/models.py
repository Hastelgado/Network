from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self',blank=True,related_name='user_following',symmetrical=False)

    def __str__(self):
        return f"User-id:{self.id},   Name:{self.username}"

class Post(models.Model):
    content = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    users_liked = models.ManyToManyField(User, blank=True, related_name="posts_liked")

    def __str__(self):
        return f"Post-id:{self.id},   Post-time:{self.time.strftime('%b %d %Y, %I:%M %p')},   By-User:{self.user.username}"


#class Like(models.Model):
#    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_likes")
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
#
#   def __str__(self):
#       return f"Like-id:{self.id},   Like-by:{self.user.username},   On-post:{self.post.id}"
