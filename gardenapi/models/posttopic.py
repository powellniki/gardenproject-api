from django.db import models
from .post import Post
from .topic import Topic



class PostTopic(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name="posttopics")
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name="posttopics")