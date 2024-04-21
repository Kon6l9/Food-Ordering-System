from django.utils import timezone

from decimal import Decimal
from django.db import models
from django.conf import settings

from account.models import RestaurantProfile

class Menu(models.Model):
    restaurant = models.OneToOneField(RestaurantProfile, on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to='menus_images/', null=True, blank=True)


       
class Section(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='sections',
    )
    name = models.CharField(max_length=30)

class FoodItem(models.Model):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='foods',
    )
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) 
    image = models.ImageField(upload_to='foods_images/', null=True, blank=True)


class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'Cart'),
        ('request', 'Request'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('account.RestaurantProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food_item = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return Decimal(self.food_item.price) * self.quantity
    
class Booking(models.Model):
    STATUS_CHOICES = (
        ('request', 'Request'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('account.RestaurantProfile', on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='request')

    def __str__(self):
        return f"Booking at {self.restaurant.name} on {self.date} at {self.time}"