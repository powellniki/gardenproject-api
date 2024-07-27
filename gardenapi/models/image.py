from django.db import models
from .post import Post

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_path = models.ImageField(upload_to='images', width_field=None, max_length=None, null=True)