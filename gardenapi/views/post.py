from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import models
from gardenapi.models import Post, Gardener, Topic, Comment




class Posts(ViewSet):
    """Request handlers for Posts in the Garden Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    def list(self, request):
        filter_type = request.query_params.get('filter', None)

        if filter_type == 'recent':
            posts = Post.objects.order_by('-created_date')
        elif filter_type == 'popular':
            posts = Post.objects.annotate(comment_count=models.Count('comments')).order_by('-comment_count')
        else:
            posts = Post.objects.all()

        serialized = PostSerializer(posts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name',)

class GardenerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()

    class Meta:
        model = Gardener
        fields = ('username',)

class PostSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)
    comment_count = serializers.SerializerMethodField()
    topics = TopicSerializer(many=True)

    class Meta:
        model = Post
        url = serializers.HyperlinkedIdentityField(view_name="post", lookup_field="id")
        fields = ('created_date', 'title', 'description', 'gardener', 'comment_count', 'topics',)
        depth = 1

    def get_comment_count(self, obj):
        # calculate the number of comments for the post
        return Comment.objects.filter(post=obj).count()