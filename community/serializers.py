from rest_framework import serializers
from .models import *

class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'created_at',
            'updated_at',
            'image',
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

    like = serializers.SerializerMethodField(read_only=True)
    # 이거는 확인용임(추후에 없앨수도)
    def get_like(self, instance):
        likes = instance.like.all()
        return [like.username for like in likes]
    
    image = serializers.ImageField(use_url=True, required=False)
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            'id',
            'writer',
            'created_at',
            'updated_at',
            'like_num',
        ]

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField(read_only = True)
    def get_post(self, instance):
        post = instance.post
        return post.id
    
    writer = serializers.SerializerMethodField(read_only = True)
    def get_writer(self, instance):
        return instance.writer.username
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', 'writer']