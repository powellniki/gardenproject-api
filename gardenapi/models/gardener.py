from django.db import models
from django.contrib.auth.models import User


class Gardener(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    location = models.CharField(max_length=25, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        null=True, 
        blank=True, 
        upload_to='images/', 
        height_field=None, 
        width_field=None, 
        max_length=None
    )

    @property
    def username(self):
        return self.user.username