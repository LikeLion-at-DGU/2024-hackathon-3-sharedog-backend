from rest_framework import serializers
from .models import *
from accounts.models import *
from community.models import *
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

class TotaltestSerializer(serializers.ModelSerializer):
    size = SizetestSerializer()
    age_group = AgetestSerializer()
    weight_group = WeighttestSerializer()
    is_vaccinated = VaccinetestSerializer()
    has_disease = DiseasetestSerializer()
    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    class Meta:
        model = Totaltest
        fields = '__all__'



class DogProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogProfile
        fields = ['id','dogname']
        
# class ProfileSerializer(serializers.ModelSerializer):
#     dogs = DogProfileSerializer(many=True, read_only=True)

#     class Meta:
#         model = Profile
#         fields = ['id','name','image','dogs']
class PostSerializer(serializers.ModelSerializer):

    image_1 = serializers.SerializerMethodField() 
    class Meta:
        model = Post
        fields = ['id','blood','region','title','content','image_1','created_at']

    def get_image_1(self, obj):
        request = self.context.get('request')
        if request and obj.image_1:
            # 절대 URL 생성
            return request.build_absolute_uri(obj.image_1.url)
        return None