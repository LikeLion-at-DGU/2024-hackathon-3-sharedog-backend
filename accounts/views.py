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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class KakaoLogin(APIView):
    def post(self, request):
        access_token = request.data.get("access_token")
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

        if not email:
            return Response({"error": "Email not provided by Kakao"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 생성 또는 기존 사용자 가져오기
        user, created = User.objects.get_or_create(username=email, defaults={"email": email})

        if created:
            user.set_unusable_password()
            user.save()

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view"}, status=status.HTTP_200_OK)


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