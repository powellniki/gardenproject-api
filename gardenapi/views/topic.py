from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from gardenapi.models import Topic

class Topics(ViewSet):
    """Request handlers for Topics in the Garden Platform"""

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    def list(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name',)