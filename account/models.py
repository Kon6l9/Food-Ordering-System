from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

USER_TYPE_CHOICES = [
    ('restaurant', 'Restaurant'),
    ('customer', 'Customer'),
    ('admin', 'Admin'),
    ]
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)

    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class RestaurantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant_profile')
    restaurant_name = models.CharField(max_length=30, default='Default Restaurant')
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user.email

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    first_name = models.CharField(max_length=50,default='first name')
    last_name = models.CharField(max_length=50,default='last name')
    phone = models.CharField(max_length=20)   

    def __str__(self):
        return self.user.email
    
