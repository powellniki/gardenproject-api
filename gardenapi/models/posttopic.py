from django.db import models
from .topic import Topic



class PostTopic(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="posttopics")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="posttopics")