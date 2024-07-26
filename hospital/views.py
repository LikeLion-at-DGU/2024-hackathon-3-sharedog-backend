from django.shortcuts import get_object_or_404, render
from .models import *
from rest_framework import viewsets, mixins
from .serializers import HospitalSerializer, DogSerializer, ReservationSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

    # action을 이용해서 특정 지역에 해당하는 filtering

class DogViewSet(viewsets.ModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def list(self, request, user_id=None):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
class ReservationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class HospitalReservationVieSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def list(self, request, hospital_id=None):
        hospital = get_object_or_404(Hospital, id=hospital_id)
        queryset = self.filter_queryset(self.get_queryset().filter(hospital=hospital))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, hospital_id=None):
        hospital = get_object_or_404(Hospital, id=hospital_id)
        user = self.request.user
        dog = Dog.objects.filter(user=user).first()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hospital=hospital, dog=dog)
        return Response(serializer.data)
