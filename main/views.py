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
    def get(self, request, region=None):
        # 모든 UserProfile 객체를 가져옵니다.
        user = self.request.user
        profiles = UserProfile.objects.filter(user=user)
        profiles_data = UserProfileSerializer(profiles, many=True, context={'request': request}).data
        
        # region이 주어지면 해당 지역의 Post를 가져옵니다.
        if region:
            posts = Post.objects.filter(region=region).order_by('-created_at')[:2]
        else:
            # region이 없으면 모든 Post를 가져옵니다.
            posts = Post.objects.filter(region='서울').order_by('-created_at')[:2]
        posts_data = PostSerializer(posts, many=True, context={'request': request}).data

        data = {
            'profiles': profiles_data,
            'posts': posts_data,
        }
        return Response(data)

    @action(methods=["GET"], detail=False, url_path='region/(?P<region>[^/.]+)')
    def filter_by_region(self, request, region=None):
        # 'region'에 따라 필터링합니다.
        return self.get(request, region=region)