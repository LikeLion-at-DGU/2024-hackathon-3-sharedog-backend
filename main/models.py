from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sizetest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    SIZE_CHOICES = [
        ('SM', '소형견'),
        ('LG', '대형견'),
    ]

    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    def __str__(self):
        return self.get_size_display()
    
class Agetest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    AGE_CHOICES = [
        ('UNDER_18M', '18개월 미만'),
        ('18M_TO_8Y', '18개월~8살'),
        ('OVER_9Y', '9살 이상'),
    ]

    age_group = models.CharField(max_length=10, choices=AGE_CHOICES)
    def __str__(self):
        return self.get_age_group_display()
    
class Weighttest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    WEIGHT_CHOICES = [
        ('UNDER_20KG', '20kg 이하'),
        ('OVER_20KG', '20kg 이상'),
    ]

    weight_group = models.CharField(max_length=10, choices=WEIGHT_CHOICES)

    def __str__(self):
        return self.get_weight_group_display()
    
class Vaccinetest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    VACCINE_CHOICES = [
        ('YES', '네'),
        ('NO', '아니요'),
    ]

    is_vaccinated = models.CharField(max_length=3, choices=VACCINE_CHOICES)

    def __str__(self):
        return self.get_is_vaccinated_display()  

class Diseasetest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    DISEASE_CHOICES = [
        ('YES', '네'),
        ('NO', '아니요'),
    ]

    has_disease = models.CharField(max_length=3, choices=DISEASE_CHOICES)

    def __str__(self):
        return self.get_has_disease_display()
    
class Totaltest(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    sizetest = models.OneToOneField(Sizetest, on_delete=models.CASCADE)
    agetest = models.OneToOneField(Agetest, on_delete=models.CASCADE)
    weighttest = models.OneToOneField(Weighttest, on_delete=models.CASCADE)
    vaccinetest = models.OneToOneField(Vaccinetest, on_delete=models.CASCADE)
    diseasetest = models.OneToOneField(Diseasetest, on_delete=models.CASCADE)
