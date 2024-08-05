from rest_framework import serializers
from accounts.models import *
from community.models import *
from hospital.models import *
class AddDogProfileSerilizer(serializers.ModelSerializer):

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
    
class MypageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname','email']

class ReservationSerializer(serializers.ModelSerializer):
    hospital = serializers.CharField(source='hospital.name', read_only=True)
    dog = serializers.CharField(source='dog.dog_name', read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, instance):
        return instance.user.nickname
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['hospital', 'user', 'dog']
