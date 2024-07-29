from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.files.base import ContentFile
import base64
from django.utils import timezone
from rest_framework.decorators import action
from gardenapi.models import Post, Gardener, PostTopic, Topic, Image
from .serializers import PostCreateSerializer, PostSerializer





class Posts(ViewSet):
    """Request handlers for Posts in the Garden Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):

        # make sure gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Initialize the create serializer with request data and context
        serializer = PostCreateSerializer(data=request.data, context={'request': request})
        
        # Validate the serializer
        if serializer.is_valid():
            validated_data = serializer.validated_data
            title = validated_data.get('title')
            description = validated_data.get('description')
            posttopics_ids = validated_data.get('posttopics', [])

            # Get the gardener associated with the authenticated user
            try:
                gardener = Gardener.objects.get(user=request.user)
            except Gardener.DoesNotExist:
                return Response({'error': 'Gardener does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Create and save the new post instance
            new_post = Post.objects.create(
                title=title,
                description=description,
                gardener=gardener,
                created_date=timezone.now().date()
            )

            # Establish many-to-many relationships with post-topics
            for topic_id in posttopics_ids:
                try:
                    topic = Topic.objects.get(id=topic_id)
                    PostTopic.objects.create(post=new_post, topic=topic)
                except Topic.DoesNotExist:
                    continue
            
            # Handles Image Uploads
            if 'image_path' in request.FILES:
                for image in request.FILES.getlist('image_path'):
                    Image.objects.create(post=new_post, image_path=image)

            # Serialize and return the new post instance
            response_serializer = PostSerializer(new_post, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors if any
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None):

        # make sure gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            post = Post.objects.get(pk=pk)

            # Check if the authenticated user has permission to edit the post
            if post.gardener.user != request.user:
                return Response({'message': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)
            
            
            # validate the serializer
            serializer = PostCreateSerializer(post, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                validated_data = serializer.validated_data
                post.title = validated_data.get('title', post.title)
                post.description = validated_data.get('description', post.description)
                
                # Get the gardener associated with the authenticated user
                try:
                    gardener = Gardener.objects.get(user=request.user)
                except Gardener.DoesNotExist:
                    return Response({'error': 'Gardener does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
                post.gardener = gardener

                post.save()

                # clear existing PostTopic relationships
                PostTopic.objects.filter(post=post).delete()

                # establish new PostTopic relationships
                posttopic_ids = serializer.validated_data.get('posttopics', [])
                for topic_id in posttopic_ids:
                    try:
                        topic = Topic.objects.get(id=topic_id)
                        PostTopic.objects.create(post=post, topic=topic)
                    except Topic.DoesNotExist:
                        continue
                
                # Clear existing image relationships
                # Image.objects.filter(post=post).delete()

                # Handle new image Uploads
                if 'image_path' in request.FILES:
                    for image in request.FILES.getlist('image_path'):
                        Image.objects.create(post=post, image_path=image)

                # Serialize and return the new post instance
                response_serializer = PostSerializer(post, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Post.DoesNotExist:
            return Response({'message': 'The post you are trying to edit does not exist'}, status=status.HTTP_404_NOT_FOUND)



    def destroy(self, request, pk=None):
        
        # make sure the gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            post = Post.objects.get(pk=pk)
            if post.gardener.user == request.user:
                post.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You do not own that post'}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        filter_type = request.query_params.get('filter', None)
        topic_id = request.query_params.get('topic', None)
        gardener_id = request.query_params.get('gardener', None)

        if topic_id:
            posts = Post.objects.filter(posttopics__topic__id=topic_id)
        else:
            posts = Post.objects.all()

        if filter_type == 'recent':
            posts = Post.objects.order_by('-created_date')
        elif filter_type == 'popular':
            posts = Post.objects.annotate(comment_count=models.Count('comments')).order_by('-comment_count')
        # else:
        #     posts = Post.objects.all()

        if gardener_id:
            posts = Post.objects.filter(gardener=gardener_id)
        

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



