from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, PostCommentViewSet, LikePostViewSet, UserCommentViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "community"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register('posts', PostViewSet, basename='posts')

like_post_router = routers.SimpleRouter(trailing_slash=False)
like_post_router.register('check', LikePostViewSet, basename='check')

my_comment_router = routers.SimpleRouter(trailing_slash=False)
my_comment_router.register('my-comments', UserCommentViewSet, basename='my-comments')

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comments')

post_comment_router = routers.SimpleRouter(trailing_slash=False)
post_comment_router.register('comments', PostCommentViewSet, basename='comments')

urlpatterns = [
    path("", include(default_router.urls)),
    path("like/", include(like_post_router.urls)),
    path('comments/', include(my_comment_router.urls)),
    path("", include(comment_router.urls)),
    path("posts/<int:post_id>/", include(post_comment_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)