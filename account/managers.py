from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django import forms

USER_TYPE_CHOICES = [
    ('restaurant', 'Restaurant'),
    ('customer', 'Customer'),
    ('admin', 'Admin'),
    ]

class CustomUserManager(BaseUserManager):
 
    '''Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.'''
    
    def create_user(self, email, password, user_type, **extra_fields):
        #Create and save a user with the given email and password.
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, user_type='admin',  **extra_fields)

