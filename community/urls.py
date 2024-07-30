from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, PostCommentViewSet, LikePostViewSet, RecommentViewSet, CommentReCommentViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "community"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register('posts', PostViewSet, basename='posts')

like_post_router = routers.SimpleRouter(trailing_slash=False)
like_post_router.register('check', LikePostViewSet, basename='check')

#my_comment_router = routers.SimpleRouter(trailing_slash=False)
#my_comment_router.register('my-comments', UserCommentViewSet, basename='my-comments')

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comments')

comment_recomment_router = routers.SimpleRouter(trailing_slash=False)
comment_recomment_router.register('recomments', CommentReCommentViewSet, basename='comment-recomments')

post_comment_router = routers.SimpleRouter(trailing_slash=False)
post_comment_router.register('comments', PostCommentViewSet, basename='comments')

recomment_router = routers.SimpleRouter(trailing_slash=False)
recomment_router.register('recomments', RecommentViewSet, basename='recomments')

urlpatterns = [
    path("", include(default_router.urls)),
    path("like/", include(like_post_router.urls)),
    #path('comments/', include(my_comment_router.urls)),
    path("", include(comment_router.urls)),
    path("posts/<int:post_id>/", include(post_comment_router.urls)),
    path("posts/<int:post_id>/comments/<int:pk>/", CommentViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='post-comment-detail'),
    path("posts/<int:post_id>/comments/<int:comment_id>/recomments/", CommentReCommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-recomments'),
    path("posts/<int:post_id>/comments/<int:comment_id>/recomments/<int:pk>/", CommentReCommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-recomment-detail'),    path("", include(recomment_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)