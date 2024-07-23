from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from gardenapi.models import Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import CommentSerializer


class Comments(ViewSet):
    """Request handlers for Comments in the Garden Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message': 'The comment you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    def list(self, request):
        chosen_post = request.query_params.get('post', None)
        comments = Comment.objects.all()
        
        if chosen_post is not None:
            comments = Comment.objects.filter(post=chosen_post)

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


