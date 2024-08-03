from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import requests
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.backends import ModelBackend
from .models import *
from .serializers import *


User = get_user_model()

# local에서 할 때는 baseurl 바꾸기
BASE_URL = "http://localhost:8000/"
# BASE_URL = "http://15.164.36.40/" 
KAKAO_CALLBACK_URI = BASE_URL + 'api/accounts/kakao/callback/'

@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    code = request.GET.get("code")
    
    # Access Token Request
    try:
        token_req = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": rest_api_key,
                "redirect_uri": KAKAO_CALLBACK_URI,
                "code": code
            }
        )
        token_req.raise_for_status()
        token_req_json = token_req.json()
        access_token = token_req_json.get("access_token")
        refresh_token = token_req_json.get("refresh_token")

        # Email Request
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_request.raise_for_status()
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        profile_info = {
            "email": email,
            "nickname": kakao_account.get("profile", {}).get("nickname"),
            "profile_image": kakao_account.get("profile", {}).get("profile_image_url"),
        }
        nickname = kakao_account.get("profile", {}).get("nickname")
        # profile = kakao_account.get("profile", {}).get("profile_image_url")
        print(nickname)
        # print(profile)
        # Signup or Signin
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = nickname
            user.save()

        # Save the Kakao access token in SocialAccount (Optional)
        social_account, created = SocialAccount.objects.update_or_create(
            provider='kakao',
            uid=email,  # Using email as uid for simplicity, or use a more appropriate field
            defaults={'user': user, 'extra_data': {'access_token': access_token}}
        )

        
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        jwt_access_token = refresh.access_token 
        
        # Save the Kakao access token in SocialAccount (Optional)
        response_data = {
            "message": "Success",
            "profile_info": profile_info,
            "access_token": str(jwt_access_token),
            "refresh_token": str(refresh),
        }
        response = JsonResponse(response_data)
        cookie_max_age = 3600 * 24 * 14  # 14 days
        response.set_cookie('access_token', str(jwt_access_token), max_age=3600, httponly=True, samesite='Lax')
        response.set_cookie('refresh_token', str(refresh), max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response

    except requests.RequestException as e:
        return JsonResponse({"err_msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"err_msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8080/login"

@api_view(["POST"])

def logout(request):
    access_token = None
    
    # Fetch the user's Kakao access token
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    
    if access_token:
        # 액세스 토큰을 블랙리스트에 추가합니다.
        BlacklistedToken.objects.create(token=access_token)
    
    if refresh_token:
        # 리프레시 토큰을 블랙리스트에 추가합니다.
        BlacklistedToken.objects.create(token=refresh_token)

    response = JsonResponse({"message": "Successfully logged out"})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')  # If you're using refresh tokens in cookies
    response.delete_cookie('sessionid')  # Delete the sessionid cookie
    return response

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email
    })