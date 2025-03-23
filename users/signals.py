from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'director':
            group, _ = Group.objects.get_or_create(name='Directors')
            instance.groups.add(group)
        elif instance.role == 'coach':
            group, _ = Group.objects.get_or_create(name='Coaches')
            instance.groups.add(group)
        elif instance.role == 'guest':
            group, _ = Group.objects.get_or_create(name='Guests')
            instance.groups.add(group)
