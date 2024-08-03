from django.urls import path, include
from rest_framework import routers
from .views import *

from django.conf.urls.static import static
from django.conf import settings

app_name = "accounts"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("dogprofiles",DogProfileViewSet, basename="dogprofiles")

urlpatterns = [
    path("",include(default_router.urls)),
    path('auth/kakao/', KakaoLogin.as_view(), name='kakao_login'),
    path('protected/', protected_view, name='protected_view'),
    path('', include('dj_rest_auth.urls')),
    path('registration', include('dj_rest_auth.registration.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)