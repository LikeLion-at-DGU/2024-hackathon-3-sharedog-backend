from accounts.models import *
from community.models import *
from rest_framework import viewsets, mixins
from .serializers import AddDogProfileSerilizer, MyPostSerializer, MypageSerializer
from rest_framework.response import Response
from community.models import Post, Comment
from rest_framework.permissions import IsAuthenticated
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

class LikePostViewSet(viewsets.ModelViewSet):  # ReadOnly로 설정하여 읽기 전용
    serializer_class = MyPostSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        # 현재 요청을 보낸 사용자를 가져옵니다.
        user = self.request.user
        # 사용자가 좋아요를 누른 게시물만 반환합니다.
        liked_posts = Post.objects.filter(like=user)
        return liked_posts
class CommentedPostViewSet(viewsets.ModelViewSet):  # ReadOnly로 설정하여 읽기 전용
    serializer_class = MyPostSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        # 현재 요청을 보낸 사용자를 가져옵니다.
        user = self.request.user
        # 사용자가 작성한 댓글의 게시물만 반환합니다.
        commented_posts = Post.objects.filter(comments__writer=user).distinct()
        return commented_posts
    
class MypageViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = MypageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        return UserProfile.objects.filter(user=user)