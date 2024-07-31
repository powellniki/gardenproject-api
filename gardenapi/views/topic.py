from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gardenapi.models import Topic
from .serializers import TopicSerializer

class Topics(ViewSet):
    """Request handlers for Topics in the Garden Platform"""

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        try:
            topic = Topic.objects.get(pk=pk)
            serializer = TopicSerializer(topic, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Topic.DoesNotExist:
            return Response({'message': 'The topic you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    def list(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


