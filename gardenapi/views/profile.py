from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gardenapi.models import Gardener
from .serializers import GardenerSerializer



class Profiles(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            profile = Gardener.objects.get(pk=pk)
            serializer = GardenerSerializer(profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Gardener.DoesNotExist:
            return Response({'error': 'Gardener does not exist'}, status=status.HTTP_404_NOT_FOUND)