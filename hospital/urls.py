from django.urls import path, include
from rest_framework import routers
from .views import HospitalViewSet, DogViewSet, ReservationUserViewSet, ReservationViewSet, HospitalReservationViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "hospital"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register('home', HospitalViewSet, basename='home')

dog_router = routers.SimpleRouter(trailing_slash=False)
dog_router.register('dog', DogViewSet, basename='dog')

reservation_check_router = routers.SimpleRouter(trailing_slash=False)
reservation_check_router.register('check', ReservationUserViewSet, basename='check')

reservation_router = routers.SimpleRouter(trailing_slash=False)
reservation_router.register('reservation', ReservationViewSet, basename='reservation')

hospital_reservation_router = routers.SimpleRouter(trailing_slash=False)
hospital_reservation_router.register('reservation', HospitalReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(dog_router.urls)),
    path('reservation/', include(reservation_check_router.urls)),
    path('', include(reservation_router.urls)),
    path('<int:hospital_id>/', include(hospital_reservation_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)