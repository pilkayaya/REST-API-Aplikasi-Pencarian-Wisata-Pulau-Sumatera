from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import (
    User, StatusModel, Profile,
)

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance,
            status = StatusModel.objects.first(), user_create = instance)