from rest_framework import serializers
from django.contrib.auth.models import User
from gardenapi.models import Post, Gardener, PostTopic, Topic, Comment


class GardenerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()

    class Meta:
        model = Gardener
        fields = ('username',)


class CommentSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('post', 'comment', 'date', 'gardener',)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name',)


class PostCreateSerializer(serializers.ModelSerializer):
    posttopics = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'description', 'posttopics',)


class PostSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)
    comment_count = serializers.SerializerMethodField()
    topics = TopicSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    posttopics = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ('created_date', 'title', 'description', 'gardener', 'comment_count', 'comments', 'topics', 'posttopics',)
        depth = 1

    def get_comment_count(self, obj):
        # calculate the number of comments for the post
        return Comment.objects.filter(post=obj).count()