from rest_framework import serializers
from .models import *
from accounts.serializers import DogProfileSerializer

class HospitalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            'id',
            'name',
            'region',
            'place',
            'created_at',
            'updated_at',
            'image',
        ]

class HospitalSerializer(serializers.ModelSerializer):
    reservation = serializers.SerializerMethodField(read_only=True)
    
    def get_reservation(self, instance):
        serializer = ReservationSerializer(instance.reservations, many=True)
        return serializer.data
    
    def validate(self, data):
        if 'region' not in data or not data['region']:
            raise serializers.ValidationError({"region": "Region is required."})
        return data

    class Meta:
        model = Hospital
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

class ReservationSerializer(serializers.ModelSerializer):
    hospital = serializers.ReadOnlyField(source='hospital.name')
    dog = DogProfileSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.nickname')
    kingdog_info = serializers.ReadOnlyField(source='dog.kingdog_info')
    dateHead = serializers.SerializerMethodField()
    dateContent = serializers.SerializerMethodField()

    def get_dateHead(self, obj):
        days = ['월', '화', '수', '목', '금', '토', '일']
        selected_date = obj.selectedDate
        day_of_week = days[selected_date.weekday()]
        return selected_date.strftime(f"%Y.%m.%d ({day_of_week})")

    def get_dateContent(self, obj):
        days = ['월', '화', '수', '목', '금', '토', '일']
        selected_date = obj.selectedDate
        day_of_week = days[selected_date.weekday()]
        return selected_date.strftime(f"%m월 %d일 {day_of_week}요일")
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        # kingdog 값이 True인 dog 가져오기
        kingdog = DogProfile.objects.filter(owner=user_profile, kingdog=True).first()
        if not kingdog:
            raise serializers.ValidationError("kingdog를 찾을 수 없습니다.")
        
        validated_data['user'] = user_profile
        validated_data['dog'] = kingdog
        reservation = Reservation.objects.create(**validated_data)
        return reservation

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['hospital', 'user']