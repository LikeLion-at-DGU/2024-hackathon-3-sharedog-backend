from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.user.username

# class Profile(models.Model):
    
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=40)
#     image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

#     phone = models.CharField(max_length=40)
#     email = models.CharField(max_length=40)
    

class DogProfile(models.Model):

    id = models.AutoField(primary_key=True)
    dogname = models.CharField(max_length=40)
    owner = models.ForeignKey(UserProfile, related_name='dogs', on_delete=models.CASCADE,null=True,blank=True)
    GENDER_M = "수컷"
    GENDER_N = "중성화"
    GENDER_F = "암컷"
    GENDER_CHOICES = (
        (GENDER_M, "수컷"),
        (GENDER_N, "중성화"),
        (GENDER_F, "암컷"),
    )
    
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    dog_age = models.IntegerField()
    dog_weight = models.FloatField(max_length=50)
    DOG_BLOOD_TYPES = [
        ('DEA 1-', 'DEA 1-'),
        ('DEA 1.1', 'DEA 1.1'),
        ('DEA 1.2', 'DEA 1.2'),
        ('DEA 3', 'DEA 3'),
        ('DEA 4', 'DEA 4'),
        ('DEA 5', 'DEA 5'),
        ('DEA 7', 'DEA 7'),
    ]

    # 다른 필드들
    dog_blood = models.CharField(max_length=15, choices=DOG_BLOOD_TYPES)