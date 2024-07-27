from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from .models import Sizetest, Agetest, Weighttest, Vaccinetest, Diseasetest, Totaltest
from .serializers import SizetestSerializer, AgetestSerializer, WeighttestSerializer, VaccinetestSerializer, DiseasetestSerializer, TotaltestSerializer
from rest_framework.response import Response

class SizetestViewSet(viewsets.ModelViewSet):
    queryset = Sizetest.objects.all()
    serializer_class = SizetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class AgetestViewSet(viewsets.ModelViewSet):
    queryset = Agetest.objects.all()
    serializer_class = AgetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class WeighttestViewSet(viewsets.ModelViewSet):
    queryset = Weighttest.objects.all()
    serializer_class = WeighttestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class VaccinetestViewSet(viewsets.ModelViewSet):
    queryset = Vaccinetest.objects.all()
    serializer_class = VaccinetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
class DiseasetestViewSet(viewsets.ModelViewSet):
    queryset = Diseasetest.objects.all()
    serializer_class = DiseasetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
        

class TotaltestViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        sizetest = Sizetest.objects.filter(writer=self.request.user).last()
        agetest = Agetest.objects.filter(writer=self.request.user).last()
        weighttest = Weighttest.objects.filter(writer=self.request.user).last()
        diseasetest = Diseasetest.objects.filter(writer=self.request.user).last()
        vaccinetest = Vaccinetest.objects.filter(writer=self.request.user).last()

        # Combine and serialize separately
        # For example, you could use different serializers for each queryset
        data = {
            'sizetest': SizetestSerializer(sizetest).data,
            'agetest': AgetestSerializer(agetest).data,
            'weighttest': WeighttestSerializer(weighttest).data,
            'diseasetest': DiseasetestSerializer(diseasetest).data,
            'vaccinetest': VaccinetestSerializer(vaccinetest).data,
        }
        return Response(data)