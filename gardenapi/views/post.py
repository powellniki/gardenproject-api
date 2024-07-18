from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from gardenapi.models import Post, Gardener




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
        posts = Post.objects.all()
        serialized = PostSerializer(posts, many=True,)
        return Response(serialized.data, status=status.HTTP_200_OK)
    


class PostOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class GardenerSerializer(serializers.ModelSerializer):
    user = PostOwnerSerializer(many=False)

    class Meta:
        model = Gardener
        fields = ('user',)


class PostSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)

    class Meta:
        model = Post
        url = serializers.HyperlinkedIdentityField(view_name="post", lookup_field="id")
        fields = ('created_date', 'title', 'description', 'gardener', 'comment_count',)
        depth = 1