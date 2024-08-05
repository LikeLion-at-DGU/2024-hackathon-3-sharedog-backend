from django.urls import path, include
from rest_framework import routers
from .views import *

from django.conf.urls.static import static
from django.conf import settings

app_name = "accounts"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("dogprofiles",DogProfileViewSet, basename="dogprofiles")

registration_router = routers.SimpleRouter(trailing_slash=False)
registration_router.register("regist",RegistrationViewSet, basename="regist")

urlpatterns = [
    path("",include(default_router.urls)),
    path('auth/kakao/', KakaoLogin.as_view(), name='kakao_login'),
    path('protected/', protected_view, name='protected_view'),
    path('check-status', check_user_status, name='check-user-status'),
    path('', include('dj_rest_auth.urls')),
    path('registration', include('dj_rest_auth.registration.urls')),
    path('', include(registration_router.urls)),
]