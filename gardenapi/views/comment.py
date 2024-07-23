from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponseServerError
from django.utils import timezone
from gardenapi.models import Comment, Gardener, Post
from .serializers import CommentSerializer


class Comments(ViewSet):
    """Request handlers for Comments in the Garden Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        # get the gardener instance associated with the authenticated user
        gardener = Gardener.objects.get(user=request.auth.user)

        # get the object instance for the post
        post_id = request.data["post_id"]
        post_instance = Post.objects.get(pk=post_id)

        # create a new comment instance and assign property values
        new_comment = Comment()
        new_comment.comment = request.data['comment']
        new_comment.post = post_instance
        new_comment.gardener = gardener
        new_comment.date=timezone.now().date()

        try:
            new_comment.save()
            serializer = CommentSerializer(new_comment, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message': 'The comment you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None):
        
        # make sure the gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            comment = Comment.objects.get(pk=pk)

            # Check if the authenticated user has permission to edit the comment
            if comment.gardener.user != request.user:
                return Response({'message': 'You do not have permission to edit this comment'}, status=status.HTTP_403_FORBIDDEN)

            # validate the serializer
            serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                validated_data = serializer.validated_data
                comment.comment = validated_data.get('comment', comment.comment)
                comment.save()

                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Comment.DoesNotExist:
            return Response({'message': 'The comment you are trying to edit does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):

        # make sure the gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # delete the comment
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.gardener.user == request.user:
                comment.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            
            return Response({'message': 'You do not have permission to edit this comment'}, status=status.HTTP_403_FORBIDDEN)

        except Comment.DoesNotExist:
            return Response({'message': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)



    def list(self, request):
        chosen_post = request.query_params.get('post', None)
        comments = Comment.objects.all()

        if chosen_post is not None:
            comments = Comment.objects.filter(post=chosen_post)

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


