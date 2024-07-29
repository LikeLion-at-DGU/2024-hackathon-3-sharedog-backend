from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import Profile, DogProfile
from .serializers import ProfileSerializer, DogProfileSerializer

from django.shortcuts import get_list_or_404

# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) 

        profile = serializer.instance
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

class DogProfileViewSet(viewsets.ModelViewSet):
    queryset = DogProfile.objects.all()
    serializer_class = DogProfileSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) 

        dogprofile = serializer.instance
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()