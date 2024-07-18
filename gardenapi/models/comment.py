from django.db import models
from .post import Post
from django.utils import timezone


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name="comments")
    comment = models.CharField(max_length=1000)
    date = models.DateField(default=timezone.now)