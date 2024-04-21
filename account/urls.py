from django.urls import path
from . import views 
from .views import signUp
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from account.views import custom_404_handler
from django.urls import path, include

handler404 = 'account.views.custom_404_handler'
urlpatterns = [
  path('signup/', views.signUp, name='signup'),
  path('login/', views.logIn, name='login'),
  path('logout/', views.logOut, name='logout'),
  path('customerprofile/<int:id>/', views.CustomerProfileView, name='customerprofile'),
  path('restaurantprofile/<int:id>/', views.RestaurantProfileView, name='restaurantprofile'),
  path('', include('main.urls')),



]