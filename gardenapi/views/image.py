from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gardenapi.models import Image
from .serializers import ImageSerializer

class Images(ViewSet):

    def destroy(self, request, pk=None):
        
        # make sure the gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            image = Image.objects.get(pk=pk)
            image.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Image.DoesNotExist:
            return Response({'message': 'Image does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        post_id = request.query_params.get('post', None)

        if post_id:
            images = Image.objects.filter(post=post_id)
        else:
            images = Image.objects.all()

        serializer = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)