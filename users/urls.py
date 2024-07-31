from django.urls import path, include
from rest_framework import routers

from .views import DogProfileViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "users"
dog_router = routers.SimpleRouter(trailing_slash=False)
dog_router.register('dogprofiles', DogProfileViewSet, basename='dogprofiles')

urlpatterns = [
    path('', include(dog_router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)