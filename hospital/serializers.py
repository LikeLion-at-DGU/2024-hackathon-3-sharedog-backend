from rest_framework import serializers
from .models import *

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

class DogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_user(self, instance):
        return instance.user.username

    class Meta:
        model = Dog
        fields = '__all__'
        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
        ]

class ReservationSerializer(serializers.ModelSerializer):
    hospital = serializers.CharField(source='hospital.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    dog = serializers.CharField(source='dog.dog_name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['hospital', 'user', 'dog']
