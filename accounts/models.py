from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    profile = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # related_name을 사용자 정의 값으로 변경
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                    'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permission_set',  # related_name을 사용자 정의 값으로 변경
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.email

class BlacklistedToken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class DogProfile(models.Model):

    id = models.AutoField(primary_key=True)
    dogname = models.CharField(max_length=40)
    # owner = models.ForeignKey(Profile, related_name='dogs', on_delete=models.CASCADE)
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