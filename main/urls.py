from django.urls import path
from . import views 
from .views import *
from account.views import custom_404_handler

handler404 = 'account.views.custom_404_handler'
urlpatterns = [
  path('', views.home, name='home'),
  path('menu-list/', views.menuList, name='menu_list'),
  path('menu/<int:id>/', views.menuView, name='menu'),
  path('delete-section/', views.delete_section, name='delete_section'),
  path('delete-food/', views.delete_food, name='delete_food'),
  path('edit-section/', views.edit_section, name='edit_section'),
  path('edit-food/', views.edit_food, name='edit_food'),
  path('add-section/<int:menu_id>/', add_section, name='add_section'),
  path('add-food/<int:section_id>/', add_food, name='add_food'),
  path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
  path('order/<int:order_id>/confirmed/', views.order_confirmed, name='order_confirmed'),
  path('order/<int:order_id>/confirm_payment/', confirm_payment, name='confirm_payment'),
  path('order/<int:order_id>/detail/', order_detail, name='order_detail'),
  path('cart/<int:cart_id>/', cart_detail, name='cart_detail'),
  path('cart-list/', views.cart_list, name='cart_list'),

  path('restaurant-orders/', restaurant_orders, name='restaurant_orders'),
  path('restaurant-bookings/', restaurant_bookings, name='restaurant_bookings'),


  path('update-order-status/<int:order_id>/<str:new_status>/', update_order_status, name='update_order_status'),
  path('update-booking-status/<int:booking_id>/<str:new_status>/', update_booking_status, name='update_booking_status'),

  path('create-booking/<int:restaurant_id>/', views.create_booking, name='create_booking'),
  path('booking-details/<int:booking_id>/', views.booking_details, name='booking_details'),


  path('search/', menu_search, name='menu_search'),
  path('update-menu-name/<int:menu_id>/', update_menu_name, name='update_menu_name'),

  path('menu/<int:id>/update-image/', update_menu_image, name='update_menu_image'),
  path('upload_food_image/', views.upload_food_image, name='upload_food_image'),

  path('cart/<int:cart_id>/', cart_detail, name='cart_detail'),
  path('cart/<int:item_id>/adjust/<str:action>/', views.adjust_item_quantity, name='adjust_item_quantity'),
  path('cart/<int:order_id>/cancel/', cancel_order, name='cancel_order'),

  path('restaurant-statistics/', restaurant_statistics, name='restaurant_statistics'),

  ]