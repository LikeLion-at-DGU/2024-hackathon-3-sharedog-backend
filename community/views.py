from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .models import Post, Comment, Recomment
from .serializers import PostListSerializer, PostSerializer, CommentSerializer, CommentListSerializer, RecommentSerializer
from accounts.models import UserProfile
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer
    
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        post_list = Post.objects.all()
        post_list = post_list.order_by('-created_at')
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
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(writer=user_profile)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # 요청 데이터에 새로운 사진이 포함되지 않은 경우 기존 사진을 유지
        if 'image_1' not in request.data:
            data = serializer.validated_data
            data['image_1'] = instance.image_1
        
        if 'image_2' not in request.data:
            data = serializer.validated_data
            data['image_2'] = instance.image_2

        if 'image_3' not in request.data:
            data = serializer.validated_data
            data['image_3'] = instance.image_3

        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_update(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    # 게시물 안에 들어가서 좋아요 구현
    @action(methods=['POST'], detail=True)
    def likes(self, request, pk=None):
        like_post = self.get_object()
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        if user_profile in like_post.like.all():
            like_post.like.remove(user_profile)
            like_post.like_num -= 1
            like_post.save()
        else:
            like_post.like.add(user_profile)
            like_post.like_num += 1
            like_post.save()
        return Response()
    
    # 게시물 리스트에서 좋아요 구현
    # @action(methods=['POST'], detail=False)
    # def like_post(self, request):
    #     post_id = request.data.get('id')
    #     user = self.request.user
    #     user_profile = UserProfile.objects.get(user=user)
    #     try:
    #         like_post = Post.objects.get(pk=post_id)
    #         if request.user in like_post.like.all():
    #             like_post.like.remove(user_profile)
    #             like_post.like_num -= 1
    #         else:
    #             like_post.like.add(user_profile)
    #             like_post.like_num += 1
    #         like_post.save()
    #         return Response({'like_num': like_post.like_num}, status=status.HTTP_200_OK)
    #     except Post.DoesNotExist:
    #         return Response({'detail': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=["GET"], detail=False, url_path='region/(?P<region>[^/.]+)')
    def filter_by_region(self, request, region=None):
        queryset = self.get_queryset().filter(region=region)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=["GET"], detail=False, url_path='blood/(?P<blood>.+)')
    def filter_by_blood(self, request, blood=None):
        queryset = self.get_queryset().filter(blood=blood)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path='filter')
    def filter_by_region_and_blood(self, request):
        region = request.query_params.get('region', None)
        blood = request.query_params.get('blood', None)
        
        queryset = self.get_queryset()
        
        if region:
            queryset = queryset.filter(region=region)
        
        if blood:
            queryset = queryset.filter(blood=blood)
        
        serializer = PostListSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

class CommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsOwnerOrReadOnly()]
        return []
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')  # URL에서 post_id를 가져옵니다.
        post = get_object_or_404(Post, id=post_id)  # 해당 post_id로 Post 객체를 가져옵니다.
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(writer=user_profile, post=post) 
    
    @action(methods=['GET'], detail=True, url_path='recomments')
    def list_recomments(self, request, pk=None):
        comment = get_object_or_404(Comment, id=pk)
        recomments = Recomment.objects.filter(comment=comment)
        serializer = RecommentSerializer(recomments, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def add_recomment(self, request, pk=None):
        comment = get_object_or_404(Comment, id=pk)
        serializer = RecommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(comment=comment, writer=user_profile)
        return Response(serializer.data)
    '''
    def list(self, request, comment_id=None):
        comment = get_object_or_404(Comment, id=comment_id)
        queryset = self.filter_queryset(self.get_queryset().filter(comment=comment))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, comment_id=None):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comment=comment)
        return Response(serializer.data)
    '''
    

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
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(post=post, writer=user_profile)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(writer=user_profile)
    
class RecommentViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Recomment.objects.all()
    serializer_class = RecommentSerializer

class CommentReCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Recomment.objects.all()
    serializer_class = RecommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsOwnerOrReadOnly()]
        return []

    def list(self, request, post_id=None, comment_id=None):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)
        queryset = self.filter_queryset(self.get_queryset().filter(comment=comment))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, post_id=None, comment_id=None):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        serializer.save(comment=comment, writer=user_profile)
        return Response(serializer.data)
    def retrieve(self, request, post_id=None, comment_id=None, pk=None):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)
        recomment = get_object_or_404(Recomment, id=pk, comment=comment)
        serializer = self.get_serializer(recomment)
        return Response(serializer.data)
    
    def update(self, request, post_id=None, comment_id=None, pk=None):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)
        recomment = get_object_or_404(Recomment, id=pk, comment=comment)
        serializer = self.get_serializer(recomment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, post_id=None, comment_id=None, pk=None):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)
        recomment = get_object_or_404(Recomment, id=pk, comment=comment)
        recomment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LikePostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, user_id=None):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        queryset = self.filter_queryset(self.get_queryset().filter(like=user_profile))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
'''
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
'''