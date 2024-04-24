from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser, CustomerProfile, RestaurantProfile
from .managers import CustomUserManager
from django.contrib.auth.forms import UserChangeForm

USER_TYPE_CHOICES = [
    ('restaurant', 'Restaurant'),
    ('customer', 'Customer'),
    ]
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class':'form-control', 'placeholder': 'yourmail@gmail.com'
        })
        self.fields['user_type'].widget.attrs.update({
            'class':'form-control', 'placeholder': 'Customer'
        })
        self.fields['password1'].widget.attrs.update({
            'class':'form-control', 'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class':'form-control', 'placeholder': 'Confirm Password'
        })
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    email=forms.EmailField(max_length=254)
    password1= forms.CharField(widget=forms.PasswordInput)
    password2= forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = ['email', 'user_type', 'password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'yourmail@gmail.com', 'autofocus': True}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Old Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'New Password'}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm New Password'}))
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password', 'confirm_new_password']


class CustomUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = CustomUser
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class CustomerProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'first_name', 'autofocus': True}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'last_name', 'autofocus': True}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'phone', 'autofocus': True}))
    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'phone']

        

class RestaurantProfileForm(forms.ModelForm):
    restaurant_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'restaurant name', 'autofocus': True}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'phone', 'autofocus': True}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'address', 'autofocus': True}))
    class Meta:
        model = RestaurantProfile
        fields = ['restaurant_name', 'phone', 'address']
