from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib import messages
from django.urls import reverse_lazy
from requests import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from account.models import CustomUser, CustomerProfile, RestaurantProfile
from .forms import *
from django.contrib.auth import authenticate, login, logout
from main.views import *
from main.models import *

def signUp(request):
    if request.method == "POST":
      form = SignupForm(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request, "Your account is created successfully")
        new_user = authenticate(
            email = form.cleaned_data.get('email'),
            password = form.cleaned_data.get('password1')
        )
        login(request, new_user)
        return redirect('home') 
      else:
        messages.error(request,"Error")
    else:
       form=SignupForm()
    return render(request, "signup.html",{'form':form})

def logIn(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logOut(request):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect('login')


@login_required(login_url='/login/')
def CustomerProfileView(request, id):
    if request.user.id != id:
        return HttpResponseForbidden("You are not allowed to view or edit another user's profile.")

    user = get_object_or_404(CustomUser, id=id)
    customer_profile = user.customer_profile

    # Fetch data for all sections
    orders = Order.objects.filter(customer=user).exclude(status='cart')
    bookings = Booking.objects.filter(customer=user)
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        profile_form = CustomerProfileForm(request.POST, instance=customer_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')

    else:
        user_form = CustomUserForm(instance=user)
        profile_form = CustomerProfileForm(instance=customer_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'customer_profile': customer_profile,
        'orders': orders,
        'bookings': bookings
    }
    return render(request, "customerprofile.html", context)


@login_required(login_url='/login/')
def RestaurantProfileView(request, id):
    if request.user.id != id:
        return HttpResponseForbidden("You are not allowed to view or edit another user's profile.")

    user = get_object_or_404(CustomUser, id=id)
    restaurant_profile = user.restaurant_profile

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)  
        profile_form = RestaurantProfileForm(request.POST, instance=restaurant_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
    else:
        user_form = CustomUserForm(instance=user)
        profile_form = RestaurantProfileForm(instance=restaurant_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'restaurant_profile': restaurant_profile,
    }
    return render(request, "restaurantprofile.html", context)


@login_required(login_url='/login/') 
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

@login_required(login_url='/login/') 
def password_success(request):
    return render(request, "password_change_success.html")

def custom_404_handler(request, exception):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'error_message': 'Page not found. Sorry, the page you requested does not exist.',
        'exception': str(exception)  
    }
    return render(request, '404.html', context, status=404)