from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BlacklistedToken

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt_access_token')
        if not token:
            return None
        try:
            # Here you would verify the token with Kakao or your own mechanism
            # If valid, return (user, token)
            email_from_token = verify_token_with_kakao(token)  # 이 부분을 구현해야 합니다.
            user = User.objects.get(email=email_from_token)
            return (user, token)
        except Exception:
            raise AuthenticationFailed('Invalid token')

def verify_token_with_kakao(token):
    """
    Verify the Kakao access token and retrieve the associated email.
    """
    try:
        # Request user information from Kakao API
        response = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        kakao_account = data.get("kakao_account")
        
        # Check if email exists in the response
        email = kakao_account.get("email")
        if not email:
            raise AuthenticationFailed('No email found in token')

        return email

    except requests.RequestException as e:
        raise AuthenticationFailed(f"Token verification failed: {str(e)}")
    
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        
        if user_auth_tuple is None:
            return None
        
        user, token = user_auth_tuple
        
        # 토큰이 블랙리스트에 있는지 확인합니다.
        if token and BlacklistedToken.objects.filter(token=token).exists():
            return None  # 블랙리스트에 있는 경우 None을 반환하여 인증 실패
        
        return user, token  # 인증 성공 시 user와 token을 반환