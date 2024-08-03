from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=SocialAccount)
def prevent_duplicate_socialaccount(sender, instance, **kwargs):
    if SocialAccount.objects.filter(provider=instance.provider, uid=instance.uid).exists():
        raise ValueError("A SocialAccount with this provider and uid already exists.")