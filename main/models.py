from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create your models here.
class Sizetest(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    SIZE_CHOICES = [
        ('소형견', '소형견'),
        ('대형견', '대형견'),
    ]

    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    def __str__(self):
        return self.get_size_display()
    
class Agetest(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    AGE_CHOICES = [
        ('~18M', '18개월 미만이에요'),
        ('18M~8Y', '18개월 이상 8세 이하에요'),
        ('9Y~', '9살 이상이에요'),
    ]

    age_group = models.CharField(max_length=10, choices=AGE_CHOICES)
    def __str__(self):
        return self.get_age_group_display()
    
class Weighttest(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    WEIGHT_CHOICES = [
        ('~20KG', '20kg 이하에요'),
        ('20KG~', '20kg 이상이에요'),
    ]

    weight_group = models.CharField(max_length=10, choices=WEIGHT_CHOICES)

    def __str__(self):
        return self.get_weight_group_display()
    
class Vaccinetest(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    VACCINE_CHOICES = [
        ('접종', '네! 매월 챙기고 있어요'),
        ('미접종', '아니요! 매월 챙기지 못했어요'),
    ]

    is_vaccinated = models.CharField(max_length=3, choices=VACCINE_CHOICES)

    def __str__(self):
        return self.get_is_vaccinated_display()  

class Diseasetest(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    DISEASE_CHOICES = [
        ('네', '네! 앓았던 적이 있어요'),
        ('아니요', '아니요! 앓았던 적이 없어요'),
    ]

    has_disease = models.CharField(max_length=3, choices=DISEASE_CHOICES)

    def __str__(self):
        return self.get_has_disease_display()
    
class Totaltest(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizetest, on_delete=models.CASCADE)
    age_group = models.ForeignKey(Agetest, on_delete=models.CASCADE)
    weight_group = models.ForeignKey(Weighttest, on_delete=models.CASCADE)
    is_vaccinated = models.ForeignKey(Vaccinetest, on_delete=models.CASCADE)
    has_disease = models.ForeignKey(Diseasetest, on_delete=models.CASCADE)
