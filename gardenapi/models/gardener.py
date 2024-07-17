from django.db import models
from django.contrib.auth.models import User


class Gardener(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    location = models.CharField(max_length=25)
    bio = models.CharField(max_length=200)
    picture = models.ImageField()