from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerSupportToken
import hashlib


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    h = hashlib.new('sha512_256')
    h.update(instance.username)

    if created:
        CustomerSupportToken.objects.create(user=instance, token=h.hexdigest())
