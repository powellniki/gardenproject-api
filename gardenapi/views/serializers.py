from rest_framework import serializers
from django.contrib.auth.models import User
from gardenapi.models import Post, Gardener, PostTopic, Topic, Comment, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class GardenerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    # id = UserSerializer(many=False)

    class Meta:
        model = Gardener
        fields = ('userId', 'username', 'location', 'bio',)
        depth = 2


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'post', 'image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image_path and hasattr(obj.image_path, 'url'):
            return request.build_absolute_uri(obj.image_path.url)
        return None


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
    posttopics = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        required=False
        )

    class Meta:
        model = Post
        fields = ('title', 'description', 'posttopics',)


class PostSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer(many=False)
    comment_count = serializers.SerializerMethodField()
    topics = TopicSerializer(many=True)
    images = ImageSerializer(many=True, read_only=True)  # Include related images

    class Meta:
        model = Post
        fields = ('id', 'created_date', 'title', 'description', 'gardener', 'comment_count', 'topics', 'images',)
        depth = 1

    def get_comment_count(self, obj):
        # calculate the number of comments for the post
        return Comment.objects.filter(post=obj).count()