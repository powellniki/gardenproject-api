from rest_framework import serializers
from django.contrib.auth.models import User
from gardenapi.models import Post, Gardener, PostTopic, Topic, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)

class GardenerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    # id = UserSerializer(many=False)

    class Meta:
        model = Gardener
        fields = ('userId', 'username',)
        depth = 2


class CommentSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'comment', 'date', 'gardener',)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name',)


class PostCreateSerializer(serializers.ModelSerializer):
    posttopics = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'description', 'posttopics',)


class PostSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)
    comment_count = serializers.SerializerMethodField()
    topics = TopicSerializer(many=True)
    # comments = CommentSerializer(many=True, read_only=True)
    # posttopics = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'created_date', 'title', 'description', 'gardener', 'comment_count', 'topics',)
        depth = 1

    def get_comment_count(self, obj):
        # calculate the number of comments for the post
        return Comment.objects.filter(post=obj).count()