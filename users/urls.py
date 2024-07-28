from django.urls import path, include
from rest_framework import routers

from .views import DogViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "users"
dog_router = routers.SimpleRouter(trailing_slash=False)
dog_router.register('dog', DogViewSet, basename='dog')


urlpatterns = [
    path('', include(dog_router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)