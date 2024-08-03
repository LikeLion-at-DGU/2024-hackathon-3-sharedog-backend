from django.conf import settings
from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)

    REGION_TYPES = [
        (None, '지역'),
        ('서울', '서울'),
        ('경기', '경기'),
        ('인천', '인천'),
        ('강원', '강원'),
        ('경상', '경상'),
        ('충청', '충청'),
        ('전라', '전라'),
        ('제주', '제주'),
    ]
    region = models.CharField(max_length=50, choices=REGION_TYPES, default='지역')
    DOG_BLOOD_TYPES = [
        (None, '혈액형'),
        ('DEA 1-', 'DEA 1-'),
        ('DEA 1.1', 'DEA 1.1'),
        ('DEA 1.2', 'DEA 1.2'),
        ('DEA 3', 'DEA 3'),
        ('DEA 4', 'DEA 4'),
        ('DEA 5', 'DEA 5'),
        ('DEA 6', 'DEA 6'),
        ('DEA 7', 'DEA 7'),
    ]
    blood = models.CharField(max_length=30, choices=DOG_BLOOD_TYPES, default='혈액형')
    
    image_1 = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    like_num = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ForeignKey(Profile, null=True, related_name='comments', on_delete=models.CASCADE)

class Recomment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, null=False, blank=False, on_delete=models.CASCADE, related_name='recomments')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ForeignKey(Profile, null=True, related_name='recomments', on_delete=models.CASCADE)
