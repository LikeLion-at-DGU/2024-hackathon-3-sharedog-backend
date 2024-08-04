from django.db import models
from users.models import DogProfile
from django.contrib.auth.models import User

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

# Create your models here.
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
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
    tel_num = models.CharField(max_length=100)
    place = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    TIME_CHOICES = [
        ('10:00', '10시'),
        ('13:00', '13시'),
        ('15:00', '15시'),
    ]
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE,null=True)
    selectedDate = models.DateField()
    activeTime = models.CharField(max_length=5, choices=TIME_CHOICES)     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
