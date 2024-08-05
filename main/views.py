from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from .models import Sizetest, Agetest, Weighttest, Vaccinetest, Diseasetest, Totaltest
from accounts.serializers import *
from accounts.models import *
from community.models import *
from .serializers import SizetestSerializer, AgetestSerializer, WeighttestSerializer, VaccinetestSerializer, DiseasetestSerializer, TotaltestSerializer,PostSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class SizetestViewSet(viewsets.ModelViewSet):
    queryset = Sizetest.objects.all()
    serializer_class = SizetestSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(nickname=user_profile)

class AgetestViewSet(viewsets.ModelViewSet):
    queryset = Agetest.objects.all()
    serializer_class = AgetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(nickname=user_profile)

class WeighttestViewSet(viewsets.ModelViewSet):
    queryset = Weighttest.objects.all()
    serializer_class = WeighttestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(nickname=user_profile)

class VaccinetestViewSet(viewsets.ModelViewSet):
    queryset = Vaccinetest.objects.all()
    serializer_class = VaccinetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(nickname=user_profile)
class DiseasetestViewSet(viewsets.ModelViewSet):
    queryset = Diseasetest.objects.all()
    serializer_class = DiseasetestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)

        disease_instance = serializer.save(nickname=user_profile)

        latest_size = Sizetest.objects.filter(nickname=user_profile).latest('id')
        latest_age = Agetest.objects.filter(nickname=user_profile).latest('id')
        latest_weight = Weighttest.objects.filter(nickname=user_profile).latest('id')
        latest_vaccine = Vaccinetest.objects.filter(nickname=user_profile).latest('id')

        # 새로운 Totaltest 객체를 생성
        Totaltest.objects.create(
            nickname=user_profile,
            size=latest_size,
            age_group=latest_age,
            weight_group=latest_weight,
            is_vaccinated=latest_vaccine,
            has_disease=disease_instance
        )
        
class TotaltestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Totaltest.objects.all()
    serializer_class = TotaltestSerializer

class MainAPIView(APIView):
    def get(self, request, region=None):
        return Response(self.get_data(request, region))

    def get_data(self, request, region=None):
        user = request.user
        profiles = UserProfile.objects.filter(user=user)
        profiles_data = UserProfileSerializer(profiles, many=True, context={'request': request}).data
        
        kingdog_profiles = DogProfile.objects.filter(owner__user=user, kingdog=True)
        kingdog_profiles_data = DogProfileSerializer(kingdog_profiles, many=True, context={'request': request}).data

        if region:
            posts = Post.objects.filter(region=region).order_by('-created_at')[:5]
        else:
            posts = Post.objects.filter(region='서울').order_by('-created_at')[:5]
        posts_data = PostSerializer(posts, many=True, context={'request': request}).data

        return {
            'profiles': profiles_data,
            'kingdog_profiles': kingdog_profiles_data,
            'posts': posts_data,
        }

class FilterByRegionAPIView(APIView):
    def get(self, request, region=None):
        main_api_view = MainAPIView()
        data = main_api_view.get_data(request, region=region if region else '서울')
        return Response(data)