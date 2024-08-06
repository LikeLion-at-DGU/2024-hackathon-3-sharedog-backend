from rest_framework import serializers
from .models import *
from accounts.models import *
from community.models import *
from datetime import datetime, timedelta
from community.serializers import *

class SizetestSerializer(serializers.ModelSerializer):

    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, instance):
        user_profile = UserProfile.objects.get(id=instance.nickname_id)
        return user_profile.nickname
    
    class Meta:
        model = Sizetest
        fields = ['id', 'nickname','size']

class AgetestSerializer(serializers.ModelSerializer):

    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, instance):
        user_profile = UserProfile.objects.get(id=instance.nickname_id)
        return user_profile.nickname
    
    class Meta:
        model = Agetest
        fields = ['id', 'nickname', 'age_group']

class WeighttestSerializer(serializers.ModelSerializer):

    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, instance):
        user_profile = UserProfile.objects.get(id=instance.nickname_id)
        return user_profile.nickname
    
    class Meta:
        model = Weighttest
        fields = ['id', 'nickname', 'weight_group']

class VaccinetestSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, instance):
        user_profile = UserProfile.objects.get(id=instance.nickname_id)
        return user_profile.nickname
    
    class Meta:
        model = Vaccinetest
        fields = ['id', 'nickname', 'is_vaccinated']

class DiseasetestSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, instance):
        user_profile = UserProfile.objects.get(id=instance.nickname_id)
        return user_profile.nickname
    
    
    class Meta:
        model = Diseasetest
        fields = ['id', 'nickname', 'has_disease']

class TotaltestSerializer(serializers.ModelSerializer):
    size = SizetestSerializer()
    age_group = AgetestSerializer()
    weight_group = WeighttestSerializer()
    is_vaccinated = VaccinetestSerializer()
    has_disease = DiseasetestSerializer()
    nickname = serializers.SerializerMethodField(read_only=True)
    score = serializers.SerializerMethodField()
    can_blood = serializers.SerializerMethodField()

    def get_nickname(self, instance):
        user_profile = UserProfile.objects.get(id=instance.nickname_id)
        return user_profile.nickname
    

    def get_score(self, instance):
        score = 0

        # Size에 따른 점수 부여
        if instance.size.size == '소형견':
            score += 0
        elif instance.size.size == '대형견':
            score += 30

        # Age에 따른 점수 부여
        if instance.age_group.age_group == '18개월 미만이에요':
            score += 0
        elif instance.age_group.age_group == '18개월 이상 8세 이하에요':
            score += 30
        elif instance.age_group.age_group == '9세 이상이에요':
            score += 0

        # Weight에 따른 점수 부여
        if instance.weight_group.weight_group == '20kg 이하에요':
            score += 0
        elif instance.weight_group.weight_group == '20kg 이상이에요':
            score += 30

        # Vaccination에 따른 점수 부여
        if instance.is_vaccinated.is_vaccinated == '네! 매월 챙기고 있어요':
            score += 10
        elif instance.is_vaccinated.is_vaccinated == '아니요! 매월 챙기지 못했어요':
            score -= 0

        # Disease에 따른 점수 부여
        if instance.has_disease.has_disease == '네! 앓았던 적이 있어요':
            score -= 0
        elif instance.has_disease.has_disease == '아니요! 앓았던 적이 없어요':
            score += 10

        return score
    
    def get_can_blood(self, instance):
        score = self.get_score(instance)
        return "헌혈 가능" if score >= 90 else "헌혈 불가"
    
    class Meta:
        model = Totaltest
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):

    image_1 = serializers.SerializerMethodField() 
    created_at = serializers.SerializerMethodField(read_only=True)

    def get_created_at(self, instance):
        now = datetime.now(instance.created_at.tzinfo)
        time_difference = now - instance.created_at

        if time_difference < timedelta(days=1):
            if time_difference < timedelta(hours=1):
                if time_difference < timedelta(minutes=1):
                    return f"방금"
                return f"{int(time_difference.total_seconds() // 60)}분 전"
            return f"{int(time_difference.total_seconds() // 3600)}시간 전"
        else:
            return f"{time_difference.days}일 전"
    class Meta:
        model = Post
        fields = ['id','blood','region','title','content','image_1','created_at']

    # def get_image_1(self, obj):
    #     request = self.context.get('request')
    #     if request and obj.image_1:
    #         # 절대 URL 생성
    #         return request.build_absolute_uri(obj.image_1.url)
    #     return None
    
    def get_image_1(self, obj):
        post = Post.objects.filter(id=obj.id)
        serializer = PostImageSerializer(post, many=True, context=self.context)
        return serializer.data
    