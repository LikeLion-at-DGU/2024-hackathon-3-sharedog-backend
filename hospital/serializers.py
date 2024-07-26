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
        ]

class HospitalSerializer(serializers.ModelSerializer):

    reservation = serializers.SerializerMethodField(read_only=True)
    def get_reservation(self, instance):
        serializer = ReservationSerializer(instance.reservations, many=True)
        return serializer.data
    
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

    hospital = serializers.SerializerMethodField(read_only=True)
    def get_hospital(self, instance):
        hospital = instance.hospital
        return hospital.name
    
    dog = serializers.SerializerMethodField(read_only=True)
    def get_dog(self, instance):
        return instance.dog.dog_name
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['hospital', 'dog']