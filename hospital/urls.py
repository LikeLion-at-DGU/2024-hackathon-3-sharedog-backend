from django.urls import path, include
from rest_framework import routers
from .views import HospitalViewSet, ReservationViewSet, HospitalReservationViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "hospital"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register('home', HospitalViewSet, basename='home')

reservation_router = routers.SimpleRouter(trailing_slash=False)
reservation_router.register('reservation', ReservationViewSet, basename='reservation')

hospital_reservation_router = routers.SimpleRouter(trailing_slash=False)
hospital_reservation_router.register('reservation', HospitalReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(reservation_router.urls)),
    path('home/<int:hospital_id>/', include(hospital_reservation_router.urls)),
]