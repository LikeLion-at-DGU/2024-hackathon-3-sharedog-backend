from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import *
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from .serializers import HospitalListSerializer, HospitalSerializer,  ReservationSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HospitalListSerializer
        return HospitalSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        hospital_list = Hospital.objects.all()

        if search_keyword:
            if len(search_keyword) > 1:
                search_hospital_list = hospital_list.filter(name__icontains=search_keyword)
                return search_hospital_list
            else:
                raise ValidationError({'detail': '검색어는 2글자 이상 입력해주세요'})

        return hospital_list

    # action을 이용해서 특정 지역에 해당하는 filtering
    @action(methods=["GET"], detail=False)
    def seoul(self, request):
        seoul_hospital = self.filter_queryset(self.get_queryset().filter(region='서울'))
        seoul_hospital_serializer = HospitalSerializer(seoul_hospital, many=True)
        return Response(seoul_hospital_serializer.data)
    @action(methods=["GET"], detail=False)
    def gyeonggi(self, request):
        gyeonggi_hospital = self.filter_queryset(self.get_queryset().filter(region='경기'))
        gyeonggi_hospital_serializer = HospitalSerializer(gyeonggi_hospital, many=True)
        return Response(gyeonggi_hospital_serializer.data)
    @action(methods=["GET"], detail=False)
    def gyeongsang(self, request):
        gyeongsang_hospital = self.filter_queryset(self.get_queryset().filter(region='경상'))
        gyeongsang_hospital_serializer = HospitalSerializer(gyeongsang_hospital, many=True)
        return Response(gyeongsang_hospital_serializer.data)
    @action(methods=["GET"], detail=False)
    def chungcheong(self, request):
        chungcheong_hospital = self.filter_queryset(self.get_queryset().filter(region='충청'))
        chungcheong_hospital_serializer = HospitalSerializer(chungcheong_hospital, many=True)
        return Response(chungcheong_hospital_serializer.data)
    @action(methods=["GET"], detail=False)
    def jeolla(self, request):
        jeolla_hospital = self.filter_queryset(self.get_queryset().filter(region='전라'))
        jeolla_hospital_serializer = HospitalSerializer(jeolla_hospital, many=True)
        return Response(jeolla_hospital_serializer.data)
    @action(methods=["GET"], detail=False)
    def jeju(self, request):
        jeju_hospital = self.filter_queryset(self.get_queryset().filter(region='제주'))
        jeju_hospital_serializer = HospitalSerializer(jeju_hospital, many=True)
        return Response(jeju_hospital_serializer.data)
# 여기서 부터 고쳐야함
class ReservationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(user=user)

class HospitalReservationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def list(self, request, hospital_id=None):
        hospital = get_object_or_404(Hospital, id=hospital_id)
        queryset = self.filter_queryset(self.get_queryset().filter(hospital=hospital))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, hospital_id=None):
        hospital = get_object_or_404(Hospital, id=hospital_id)
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(hospital=hospital)
        headers = self.get_success_headers(serializer.data)
        
        # 새로 생성된 예약 객체를 다시 직렬화하여 반환
        new_reservation = Reservation.objects.get(id=serializer.instance.id)
        new_serializer = self.get_serializer(new_reservation)
        
        return Response(new_serializer.data, status=status.HTTP_201_CREATED, headers=headers)