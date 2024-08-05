from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import *
from .serializers import *

from django.shortcuts import get_list_or_404
import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes


class KakaoLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        access_token = request.data.get("access_token")
        #phone = request.data.get("phone")
        if not access_token:
            return Response({"error": "No access token provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 카카오 API를 통해 사용자 정보 가져오기
        kakao_response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if kakao_response.status_code != 200:
            return Response({"error": "Failed to fetch user info from Kakao"}, status=status.HTTP_400_BAD_REQUEST)

        kakao_data = kakao_response.json()
        kakao_id = kakao_data.get("id")
        email = kakao_data.get("kakao_account", {}).get("email")
        nickname = kakao_data.get("properties", {}).get("nickname")
        profile_image = kakao_data.get("properties", {}).get("profile_image")
        if not email:
            return Response({"error": "Email not provided by Kakao"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 생성 또는 기존 사용자 가져오기
        try:
            user, created = User.objects.get_or_create(username=email, defaults={"email": email})

            if created:
                user.set_unusable_password()
                user.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.nickname = nickname
            user_profile.profile_image = profile_image
            user_profile.email = email
            #user_profile.phone = phone
            user_profile.save()
        except Exception as e:
            print(f"Error creating user: {str(e)}")  # 추가된 로그
            return Response({"error": "Error creating user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        # JWT 토큰 생성
        try:
            refresh = RefreshToken.for_user(user)
        except Exception as e:
            print(f"Error creating JWT token: {str(e)}")  # 추가된 로그
            return Response({"error": "Error creating JWT token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)

    user_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_profile": user_profile_serializer.data,
    }
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_user_status(request):
    user = request.user
    if user.is_authenticated:
        user_profile = UserProfile.objects.get(user=user)
        has_dog_info = DogProfile.objects.filter(owner=user_profile).exists()
        return Response({'has_dog_info': has_dog_info})
    else:
        return Response({'error': 'User is not authenticated'},status=401)

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
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(owner=user_profile)

class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 요청을 보낸 사용자의 UserProfile만 반환합니다.
        user = self.request.user
        return UserProfile.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user

        # 이미 UserProfile이 있는지 확인합니다.
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # phone 필드를 업데이트하거나 설정합니다.
        phone = request.data.get('phone', None)
        if phone:
            user_profile.phone = phone
            user_profile.save()

        if created:
            # 프로필이 새로 생성된 경우에는 전체 프로필 데이터를 반환
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 기존 프로필이었고 phone만 업데이트된 경우
            return Response({"detail": "Profile already exists. Phone number updated."}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # 이 메서드는 더 이상 필요하지 않을 수 있습니다.
        # serializer.save(user=self.request.user)
        pass