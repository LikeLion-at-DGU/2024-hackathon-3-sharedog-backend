from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'


class Profile(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    phone = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    

class DogProfile(models.Model):

    id = models.AutoField(primary_key=True)
    dogname = models.CharField(max_length=40)
    
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
    dog_weight = models.CharField(max_length=50)
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