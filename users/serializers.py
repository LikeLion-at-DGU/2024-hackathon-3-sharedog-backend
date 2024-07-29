from rest_framework import serializers
from .models import *

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