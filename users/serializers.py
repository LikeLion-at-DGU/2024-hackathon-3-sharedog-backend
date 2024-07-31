from rest_framework import serializers
from accounts.models import *


class AddDogProfileSerilizer(serializers.ModelSerializer):

    class Meta:
        model = DogProfile
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]
