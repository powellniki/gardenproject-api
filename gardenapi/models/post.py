from django.db import models
from .gardener import Gardener
from django.utils import timezone


class Post(models.Model):
    created_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    gardener = models.ForeignKey(Gardener, on_delete=models.DO_NOTHING, related_name="posts")
