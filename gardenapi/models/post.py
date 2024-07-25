from django.db import models
from .gardener import Gardener
from django.utils import timezone
from .comment import Comment
from .posttopic import PostTopic
from .topic import Topic


class Post(models.Model):
    created_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.TextField()
    gardener = models.ForeignKey(Gardener, on_delete=models.DO_NOTHING, related_name="posts")
    
    @property
    def topics(self):
        # get the topics for a post
        post_topics = PostTopic.objects.filter(post=self)
        return [post_topic.topic for post_topic in post_topics]