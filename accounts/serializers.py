from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Profile
#         fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    phone = serializers.CharField(required=True)
    class Meta:
        model = UserProfile
        fields = ['nickname','email','phone']

    def update(self, instance, validated_data):
        # phone 필드 업데이트
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

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