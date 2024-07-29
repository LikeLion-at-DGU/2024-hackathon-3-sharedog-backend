from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Comment
from .serializers import PostListSerializer, PostSerializer, CommentSerializer

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer
    
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        post_list = Post.objects.all()
        
        if search_keyword:
            if len(search_keyword) > 1:
                search_post_list = post_list.filter(
                    Q(title__icontains=search_keyword) | 
                    Q(content__icontains=search_keyword) |
                    Q(blood__icontains=search_keyword) |
                    Q(region__icontains=search_keyword)
                ).order_by('title', 'content', 'blood', 'region')
                return search_post_list
            else:
                raise ValidationError({'detail': '검색어는 2글자 이상 입력해주세요'})

        return post_list

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
    
    @action(methods=['POST'], detail=True)
    def likes(self, request, pk=None):
        like_post = self.get_object()
        if request.user in like_post.like.all():
            like_post.like.remove(request.user)
            like_post.like_num -= 1
            like_post.save()
        else:
            like_post.like.add(request.user)
            like_post.like_num += 1
            like_post.save()
        return Response()
    
    @action(methods=['POST'], detail=False)
    def like_post(self, request):
        post_id = request.data.get('post_id')
        try:
            like_post = Post.objects.get(pk=post_id)
            if request.user in like_post.like.all():
                like_post.like.remove(request.user)
                like_post.like_num -= 1
            else:
                like_post.like.add(request.user)
                like_post.like_num += 1
            like_post.save()
            return Response({'like_num': like_post.like_num}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'detail': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    # 프론트에서 처리하는거인가봐...
    @action(methods=["GET"], detail=False)
    def filter_posts(self, request):
        region = request.query_params.get('region', None)
        blood = request.query_params.get('blood', None)
        
        queryset = self.get_queryset()
        
        if region:
            queryset = queryset.filter(region=region)
        
        if blood:
            queryset = queryset.filter(blood=blood)
        
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        queryset = self.filter_queryset(self.get_queryset().filter(post=post))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, writer=self.request.user)
        return Response(serializer.data)
    
class LikePostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, user_id=None):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset().filter(like=user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class UserCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        # 현재 사용자의 댓글들을 가져옵니다.
        user_comments = Comment.objects.filter(writer=request.user)
        
        # 해당 댓글들이 달린 포스트들을 중복 없이 가져옵니다.
        posts = Post.objects.filter(comments__in=user_comments).distinct()
        
        # 포스트들을 직렬화합니다.
        serializer = PostSerializer(posts, many=True)
        
        return Response(serializer.data)