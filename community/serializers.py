from datetime import datetime, timedelta
from rest_framework import serializers
from .models import *

class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    content = serializers.SerializerMethodField()
    def get_content(self, instance):
        return instance.content[:40]

    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        return instance.writer.username

    created_at =serializers.SerializerMethodField(read_only=True)

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

class PostSerializer(serializers.ModelSerializer):
    
    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        writer = instance.writer
        return writer.username
    
    comments = serializers.SerializerMethodField(read_only=True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data

    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()

    def validate(self, data):
        if 'blood' not in data or not data['blood']:
            raise serializers.ValidationError({"blood": "Blood type is required."})
        if 'region' not in data or not data['region']:
            raise serializers.ValidationError({"region": "Region is required."})
        return data

    like = serializers.SerializerMethodField(read_only=True)
    # 이거는 확인용임(추후에 없앨수도)
    def get_like(self, instance):
        likes = instance.like.all()
        return [like.username for like in likes]
    
    image_1 = serializers.ImageField(use_url=True, required=False)
    image_2 = serializers.ImageField(use_url=True, required=False)
    image_3 = serializers.ImageField(use_url=True, required=False)
    
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            'id',
            'writer',
            'created_at',
            'updated_at',
            'comments_cnt',
            'like_num',
        ]

class CommentListSerializer(serializers.ModelSerializer):
    recomments_cnt = serializers.SerializerMethodField()

    def get_recomments_cnt(self, instance):
        return instance.recomments.count()
    
    content = serializers.SerializerMethodField()
    def get_content(self, instance):
        return instance.content[:40]

    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        return instance.writer.username

    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(read_only = True)
    def get_post(self, instance):
        post = instance.post
        return post.id
    
    writer = serializers.SerializerMethodField(read_only = True)
    def get_writer(self, instance):
        return instance.writer.username
    
    recomments = serializers.SerializerMethodField(read_only=True)
    def get_recomments(self, instance):
        serializer = RecommentSerializer(instance.recomments, many=True)
        return serializer.data
    
    
    class Meta:
        model = Comment
        fields = ['id','post','writer','content','recomments','created_at','updated_at']
        read_only_fields = ['id', 'post', 'writer']

class RecommentSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField(read_only = True)
    def get_comment(self, instance):
        comment = instance.comment
        return comment.id
    
    writer = serializers.SerializerMethodField(read_only=True)
    def get_writer(self, instance):
        return instance.writer.username

    class Meta:
        model = Recomment
        fields = '__all__'
        read_only_fields = ['id','comment', 'writer']