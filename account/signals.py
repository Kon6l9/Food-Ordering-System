from tkinter import Menu
from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import Group
from main.models import *


# @receiver(post_migrate)
# def create_default_groups(sender, **kwargs):
#     group_names = ["Customer", "Restaurant"]
#     for group_name in group_names:
#         Group.objects.get_or_create(name=group_name)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'restaurant':
            RestaurantProfile.objects.create(user=instance)
        elif instance.user_type == 'customer':
            CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'restaurant' and hasattr(instance, 'restaurant_profile'):
        instance.restaurant_profile.save()
    elif instance.user_type == 'customer' and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()

@receiver(post_save, sender=RestaurantProfile)
def create_default_menu(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(restaurant=instance, name='Default Menu')

