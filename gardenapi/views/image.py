from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gardenapi.models import Image
from .serializers import ImageSerializer

class Images(ViewSet):

    def retrieve(self, request, pk=None):
        pass

    def list(self, request):
        post_id = request.query_params.get('post', None)

        if post_id:
            images = Image.objects.filter(post=post_id)
        else:
            images = Image.objects.all()

        serializer = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)