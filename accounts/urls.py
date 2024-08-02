from django.urls import path, include
from rest_framework import routers
from .views import ProfileViewSet,DogProfileViewSet

from django.conf.urls.static import static
from django.conf import settings

app_name = "accounts"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("profiles",ProfileViewSet, basename="profiles")
default_router.register("dogprofiles",DogProfileViewSet, basename="dogprofiles")

urlpatterns = [
    path("",include(default_router.urls)),
    path('', include('dj_rest_auth.urls')),
    path('registration', include('dj_rest_auth.registration.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)