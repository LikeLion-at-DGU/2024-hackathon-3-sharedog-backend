from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

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
