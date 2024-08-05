from datetime import datetime
from rest_framework import serializers
from accounts.models import *
from community.models import *
from hospital.models import *
from accounts.serializers import *
from django.utils.timezone import make_aware

class AddDogProfileSerilizer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.nickname', read_only=True)

    class Meta:
        model = DogProfile
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]



class MyPostSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        return instance.writer.nickname
    
    image_1 = serializers.ImageField(use_url=True, required=False)
    content = serializers.SerializerMethodField()
    def get_content(self, instance):
        if len(instance.content) > 75:
            return instance.content[:75] + '...'
        return instance.content

    class Meta:
        model = Post
        fields = [
                'id',
                'title',
                'content',
                'writer',
                'created_at',
                'updated_at',
                'image_1',
                'comments_cnt',
                'like_num',
                'blood',
                'region'
            ]

    def get_image_1(self, obj):
        request = self.context.get('request')
        if request and obj.image_1:
            # 절대 URL 생성
            return request.build_absolute_uri(obj.image_1.url)
        return None
        profile_image = UserProfile.objects.filter(user=user)
class MypageSerializer(serializers.ModelSerializer):
    #profile_image = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = [
            'id','updated_at','created_at'
        ]

class MypageReservationSerializer(serializers.ModelSerializer):
    hospital = serializers.ReadOnlyField(source='hospital.name')
    dog = DogProfileSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.nickname')
    kingdog_info = serializers.ReadOnlyField(source='dog.kingdog_info')
    dateHead = serializers.SerializerMethodField()
    dateContent = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()
    donation_status = serializers.CharField(required=False, allow_blank=True, max_length=20)

    def get_dateHead(self, obj):
        days = ['월', '화', '수', '목', '금', '토', '일']
        selected_date = obj.selectedDate
        day_of_week = days[selected_date.weekday()]
        return selected_date.strftime(f"%Y.%m.%d ({day_of_week})")

    def get_dateContent(self, obj):
        days = ['월', '화', '수', '목', '금', '토', '일']
        selected_date = obj.selectedDate
        day_of_week = days[selected_date.weekday()]
        return selected_date.strftime(f"%m월 %d일 {day_of_week}요일")
    
    def get_is_past(self, obj):
        # 현재 시간
        now = datetime.now().date()  # 현재 날짜를 datetime.date로 변환

        # selected_date가 현재 날짜를 기준으로 지났는지 확인
        return obj.selectedDate < now
    
    def update(self, instance, validated_data):
        # Update the donation status if applicable
        donation_status = validated_data.get('donation_status', None)
        if instance.is_past and donation_status == 'completed':
            instance.blood_donation_completed = True
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        # kingdog 값이 True인 dog 가져오기
        kingdog = DogProfile.objects.filter(owner=user_profile, kingdog=True).first()
        if not kingdog:
            raise serializers.ValidationError("kingdog를 찾을 수 없습니다.")
        
        blood_donation_completed = validated_data.get('blood_donation_completed', False)
        validated_data['user'] = user_profile
        validated_data['dog'] = kingdog
        reservation = Reservation.objects.create(**validated_data, blood_donation_completed=blood_donation_completed)
        return reservation

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['hospital', 'user']