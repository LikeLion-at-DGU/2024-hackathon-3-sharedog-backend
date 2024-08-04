from django.urls import path, include
from rest_framework import routers

from .views import DogProfileViewSet,MyPostViewSet,CommentedPostViewSet, MypageViewSet

from django.conf import settings
from django.conf.urls.static import static

app_name = "users"
dog_router = routers.SimpleRouter(trailing_slash=False)
dog_router.register('dogprofiles', DogProfileViewSet, basename='dogprofiles')

mypost_router = routers.SimpleRouter(trailing_slash=False)
mypost_router.register('myposts',MyPostViewSet, basename='myposts')

likepost_router = routers.SimpleRouter(trailing_slash=False)
likepost_router.register('mylikes',MyPostViewSet, basename='mylikes')

comment_post_router = routers.SimpleRouter(trailing_slash=False)
comment_post_router.register('commentposts', CommentedPostViewSet, basename='commentposts')

myprofile_router = routers.SimpleRouter(trailing_slash=False)
myprofile_router.register('myprofile',MypageViewSet, basename='myprofile')

urlpatterns = [
    path('', include(dog_router.urls)),
    path('', include(mypost_router.urls)),
    path('', include(likepost_router.urls)),
    path('', include(comment_post_router.urls)),
    path('', include(myprofile_router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)