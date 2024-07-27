from rest_framework import serializers
from .models import *

class SizetestSerializer(serializers.ModelSerializer):

    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    
    class Meta:
        model = Sizetest
        fields = ['id', 'writer','size']

class AgetestSerializer(serializers.ModelSerializer):

    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    
    class Meta:
        model = Agetest
        fields = ['id', 'writer', 'age_group']

class WeighttestSerializer(serializers.ModelSerializer):

    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    
    class Meta:
        model = Weighttest
        fields = ['id', 'writer', 'weight_group']

class VaccinetestSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    
    class Meta:
        model = Vaccinetest
        fields = ['id', 'writer', 'is_vaccinated']

class DiseasetestSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    
    class Meta:
        model = Diseasetest
        fields = ['id', 'writer', 'has_disease']
