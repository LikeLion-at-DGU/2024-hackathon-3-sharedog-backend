from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from .models import Sizetest, Agetest, Weighttest, Vaccinetest, Diseasetest, Totaltest
from accounts.models import *
from community.models import *
from .serializers import SizetestSerializer, AgetestSerializer, WeighttestSerializer, VaccinetestSerializer, DiseasetestSerializer, TotaltestSerializer, ProfileSerializer, DogProfileSerializer,PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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
        disease_instance = serializer.save(writer=self.request.user)

        latest_size = Sizetest.objects.filter(writer=self.request.user).latest('id')
        latest_age = Agetest.objects.filter(writer=self.request.user).latest('id')
        latest_weight = Weighttest.objects.filter(writer=self.request.user).latest('id')
        latest_vaccine = Vaccinetest.objects.filter(writer=self.request.user).latest('id')

        # 새로운 Totaltest 객체를 생성
        Totaltest.objects.create(
            writer=self.request.user,
            size=latest_size,
            age_group=latest_age,
            weight_group=latest_weight,
            is_vaccinated=latest_vaccine,
            has_disease=disease_instance
        )
        
class TotaltestViewSet(viewsets.ModelViewSet):
    queryset = Totaltest.objects.all()
    serializer_class = TotaltestSerializer

class MainAPIView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        #dogprofiles = DogProfile.objects.all()
        posts = Post.objects.filter(region='서울').order_by('-created_at')[:2]

        profiles_data = ProfileSerializer(profiles, many=True, context={'request': request}).data
        #dogprofiles_data = DogProfileSerializer(dogprofiles, many=True).data
        posts_data = PostSerializer(posts, many=True, context={'request': request}).data

        data = {
            'profiles': profiles_data,
            #'dogprofiles': dogprofiles_data,
            'posts': posts_data,
        }
        return Response(data)
    
