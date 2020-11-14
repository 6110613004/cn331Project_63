from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Product


@receiver(post_save, sender=User) ##Sender = Models that's going to send signals
def create_profile(sender, instance, created, **kwargs): ##created = check if this is a new one
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()