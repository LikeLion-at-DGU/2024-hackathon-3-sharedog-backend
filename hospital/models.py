from django.db import models
from django.contrib.auth.models import User

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

# Create your models here.
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    region = models.CharField(max_length=100)
    tel_num = models.CharField(max_length=100)
    place = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name
    
# Dog field 다른 곳으로 옮길수도 있음
class Dog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    kind = models.CharField(max_length=100)
    blood = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='reservations')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
