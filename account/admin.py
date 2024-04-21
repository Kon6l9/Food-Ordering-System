from django.contrib import admin
from .models import *
from main.models import *

admin.site.register((CustomUser, CustomerProfile, RestaurantProfile, Menu, Section, FoodItem, Order, OrderItem, Booking ))
