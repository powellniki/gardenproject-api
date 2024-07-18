from django.db import models
from .gardener import Gardener


class Following(models.Model):
    follower = models.ForeignKey(Gardener, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(Gardener, on_delete=models.CASCADE, related_name="followers")

    # unique_together constraint ensures that a gardener cannot follow the same gardener more than once
    class Meta:
        unique_together = ('follower', 'following')