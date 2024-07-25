from rest_framework import serializers
from .models import *

class HospitalSerializer(serializers.Modelserializer):

    class Meta:
        model = Hospital
        fields = '__all__'