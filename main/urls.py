from django.urls import path, include
from rest_framework import routers
from .views import SizetestViewSet, AgetestViewSet, WeighttestViewSet, VaccinetestViewSet, DiseasetestViewSet, TotaltestViewSet, PostViewSet

from django.conf import settings

app_name = "main"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("sizetests", SizetestViewSet, basename="sizetests")
default_router.register("agetests", AgetestViewSet, basename="agetests")
default_router.register("weighttests", WeighttestViewSet, basename="weighttests")
default_router.register("vaccinetests", VaccinetestViewSet, basename="vaccinetests")
default_router.register("diseasetests", DiseasetestViewSet, basename="diseasetests")
default_router.register("totaltests", TotaltestViewSet, basename="totaltests")
default_router.register("main",PostViewSet,basename="post")
urlpatterns = [
    path("", include(default_router.urls)),
    # path('main/', MainAPIView.as_view(), name='main-api'),
]
