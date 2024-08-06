from accounts.models import *
from community.models import *
from rest_framework import viewsets, mixins, status
from .serializers import AddDogProfileSerilizer, MyPostSerializer, MypageSerializer
from rest_framework.response import Response
from community.models import Post, Comment
from rest_framework.permissions import IsAuthenticated
from community.permissions import IsOwnerOrReadOnly
from hospital.models import Reservation
from .serializers import MypageReservationSerializer
from rest_framework.decorators import action

class DogProfileViewSet(viewsets.ModelViewSet):
    serializer_class = AddDogProfileSerilizer

    def get_queryset(self):
        # 현재 요청을 보낸 사용자의 UserProfile과 연결된 DogProfile만 반환
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        return DogProfile.objects.filter(owner=user_profile).order_by('-kingdog', 'id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        dogprofile = serializer.instance
        return Response(serializer.data)

    def perform_create(self, serializer):
        # 강아지를 생성할 때 현재 사용자의 UserProfile을 소유자로 설정
        user = self.request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        serializer.save(owner=user_profile)

class MyPostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = MyPostSerializer

    def get_queryset(self):

        user = self.request.user
        user_profile = user.userprofile
        return Post.objects.filter(writer=user_profile).order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []
    
class LikePostViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly로 설정하여 읽기 전용
    serializer_class = MyPostSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        # 현재 요청을 보낸 사용자를 가져옵니다.
        user = self.request.user
        user_profile = user.userprofile
        # 사용자가 좋아요를 누른 게시물만 반환합니다.
        liked_posts = Post.objects.filter(like=user_profile)
        return liked_posts
    
class CommentedPostViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly로 설정하여 읽기 전용
    serializer_class = MyPostSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        # 현재 요청을 보낸 사용자를 가져옵니다.
        user = self.request.user
        # 사용자가 작성한 댓글의 게시물만 반환합니다.
        user_profile = UserProfile.objects.get(user=user)
        commented_posts = Post.objects.filter(comments__writer=user_profile).distinct()
        return commented_posts

class MypageViewSet(viewsets.ModelViewSet):
    serializer_class = MypageSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
    # 현재 요청을 보낸 사용자의 UserProfile을 가져와 필터링
        user = self.request.user
        # UserProfile.objects.get(user=user) 대신
        return UserProfile.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        # 사용자가 이미 존재하는지 확인하고, 있으면 업데이트, 없으면 생성
        user = self.request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # 업데이트 또는 생성된 프로필을 직렬화
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 성공적으로 생성/업데이트된 사용자 프로필을 반환
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # 업데이트할 인스턴스를 가져오고 시리얼라이저를 통해 데이터 갱신
        user = self.request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class ReservationUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Reservation.objects.all().order_by('-selectedDate')
    serializer_class = MypageReservationSerializer

    def list(self, request, user_id=None):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        queryset = self.filter_queryset(self.get_queryset().filter(user=user_profile))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_donation_status(self, request, pk=None):
        reservation = self.get_object()
        
        serializer = MypageReservationSerializer(reservation)
        is_past = serializer.data.get('is_past', False)

        if not is_past:
            return Response({'detail': '헌혈 상태를 업데이트할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
    
        # 'Blood donation completed' 상태를 업데이트합니다.
        if 'blood_donation_completed' in data:
            value = data['blood_donation_completed']
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                else:
                    return Response({'detail': '유효하지 않은 값입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            elif not isinstance(value, bool):
                return Response({'detail': '유효하지 않은 값입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            reservation.blood_donation_completed = value
            reservation.save()
            updated_serializer = MypageReservationSerializer(reservation)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': '업데이트할 필드가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
