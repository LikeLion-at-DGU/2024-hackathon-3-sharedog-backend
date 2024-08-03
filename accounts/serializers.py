from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Profile
#         fields = '__all__'

class DogProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = DogProfile
        fields = '__all__'