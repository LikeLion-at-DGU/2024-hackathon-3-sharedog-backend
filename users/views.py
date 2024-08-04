from accounts.models import *
from rest_framework import viewsets, mixins
from .serializers import AddDogProfileSerilizer, MyPostSerializer
from rest_framework.response import Response
from community.models import Post
class DogProfileViewSet(viewsets.ModelViewSet):
    queryset = DogProfile.objects.all()
    serializer_class = AddDogProfileSerilizer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) 

        dogprofile = serializer.instance
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

class MyPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = MyPostSerializer

    def get_queryset(self):

        user = self.request.user
        return Post.objects.filter(writer=user)