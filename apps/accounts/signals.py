from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import Perfil


@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    if hasattr(instance, "perfil"):
        instance.perfil.save()
