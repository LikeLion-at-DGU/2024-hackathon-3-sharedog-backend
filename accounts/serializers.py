from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh_token'])
        data = {'access_token': str(refresh.access_token)}

        return data

class DogProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DogProfile
        fields = '__all__'