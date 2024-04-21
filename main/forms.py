from django import forms
from .models import Booking, Section, FoodItem
from .models import *

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'price', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time']
