from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from gardenapi.models import Gardener
from .serializers import GardenerSerializer



class Profiles(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            profile = Gardener.objects.get(user=pk)
            serializer = GardenerSerializer(profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Gardener.DoesNotExist:
            return Response({'error': 'Gardener does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def update(self, request, pk=None):
        # make sure gardener is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Please provide authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            profile = Gardener.objects.get(user=pk)

            # check to see if the authenticated user has permission to edit the profile
            if profile.user != request.user:
                return Response({'message': 'You do not have permission to edit this profile'}, status=status.HTTP_403_FORBIDDEN)
            
            # initialize the serializer and get the data
            serializer = GardenerSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                username = serializer.validated_data.get('user', {}).get('username')
                if username:
                    profile.user.username = username
                    profile.user.save()
                profile.location = serializer.validated_data['location']
                profile.bio = serializer.validated_data['bio']
                profile.save()

                serializer = GardenerSerializer(profile, context={'request': request})
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Gardener.DoesNotExist:
            return Response({'message': 'The gardener you are trying to edit does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
