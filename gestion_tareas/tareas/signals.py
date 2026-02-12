from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil

ADMIN_EMAIL = "diazsantiromero@gmail.com"

@receiver(post_save, sender=User)
def crear_o_guardar_perfil(sender, instance, created, **kwargs):
    if created:
        rol = 'admin' if instance.email == ADMIN_EMAIL else 'user'
        Perfil.objects.create(user=instance, rol=rol)
    else:
        if hasattr(instance, 'perfil'):
            perfil = instance.perfil
            if instance.email == ADMIN_EMAIL and perfil.rol != 'admin':
                perfil.rol = 'admin'
                perfil.save()
            elif instance.email != ADMIN_EMAIL and perfil.rol != 'user':
                perfil.rol = 'user'
                perfil.save()