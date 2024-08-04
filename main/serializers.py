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
    score = serializers.SerializerMethodField()
    can_blood = serializers.SerializerMethodField()

    def get_writer(self, instance):
        writer = instance.writer
        return writer.username

    def get_score(self, instance):
        score = 0

        # Size에 따른 점수 부여
        if instance.size.size == '소형견':
            score += 0
        elif instance.size.size == '대형견':
            score += 10

        # Age에 따른 점수 부여
        if instance.age_group.age_group == '~18M':
            score += 0
        elif instance.age_group.age_group == '18M~8Y':
            score += 5
        elif instance.age_group.age_group == '9Y~':
            score += 10

        # Weight에 따른 점수 부여
        if instance.weight_group.weight_group == '~20KG':
            score += 0
        elif instance.weight_group.weight_group == '20KG~':
            score += 10

        # Vaccination에 따른 점수 부여
        if instance.is_vaccinated.is_vaccinated == '접종':
            score += 10
        elif instance.is_vaccinated.is_vaccinated == '미접종':
            score -= 0

        # Disease에 따른 점수 부여
        if instance.has_disease.has_disease == '네':
            score -= 0
        elif instance.has_disease.has_disease == '아니요':
            score += 10

        return score
    
    def get_can_blood(self, instance):
        score = self.get_score(instance)
        return "헌혈 가능" if score >= 30 else "헌혈 불가"
    
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