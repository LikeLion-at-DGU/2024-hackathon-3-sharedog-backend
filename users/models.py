from django.db import models
from accounts.models import DogProfile
# Create your models here.

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'