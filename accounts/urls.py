from django.urls import path, include
from rest_framework import routers
from .views import *
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "accounts"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("dogprofiles",DogProfileViewSet, basename="dogprofiles")

urlpatterns = [
    path("",include(default_router.urls)),
    path('', include('dj_rest_auth.urls')),
    path('registration', include('dj_rest_auth.registration.urls')),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('kakao/logout/', logout, name='logout'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)