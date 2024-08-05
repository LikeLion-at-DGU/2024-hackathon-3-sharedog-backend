from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Profile
#         fields = '__all__'



class DogProfileSerializer(serializers.ModelSerializer):
    dog_image = serializers.ImageField(use_url=True, required=False)
    
    class Meta: 
        model = DogProfile
        fields = '__all__'


# class UserDogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserDog
#         fields = ['check_dog']

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True, required=False)
    dogs = DogProfileSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['nickname', 'profile_image','email', 'dogs']