

from tkinter import Menu
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from account.models import RestaurantProfile
from django.shortcuts import get_object_or_404, render
from .models import *
from account.models import CustomUser, CustomerProfile, RestaurantProfile
from .forms import *
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.db.models import Sum, Avg, Count, Q

from django.contrib import messages
from django.core.paginator import Paginator

from django.utils.timezone import localdate


def home(request):
    total_restaurants = RestaurantProfile.objects.count()
    total_customers = CustomerProfile.objects.count()
    total_food_items = FoodItem.objects.count()

    menus = Menu.objects.annotate(
        completed_orders=Count('restaurant__order', filter=Q(restaurant__order__status='completed'))
    ).order_by('-completed_orders')[:4]

    # Build context for all users
    context = {
        'menus': menus,
        'total_restaurants': total_restaurants,
        'total_customers': total_customers,
        'total_food_items': total_food_items,  

    }
    # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.user.user_type == 'restaurant':
            menu_id = request.user.restaurant_profile.menu.id
            return redirect('menu', menu_id)
        else:    
            return render(request, 'home.html', context)
        
    else:
        return render(request, 'home.html', context)




@login_required(login_url='/login/') 
def menuView(request, id):
    restaurant = get_object_or_404(RestaurantProfile, id=id)
    menu = restaurant.menu  # Directly accessing the menu from the restaurant
    sections = menu.sections.all()
    user = request.user

    if user.is_authenticated and hasattr(user, 'restaurant_profile'):
        # Get the menu ID of the logged-in user's restaurant
        user_menu_id = user.restaurant_profile.menu.id if user.restaurant_profile.menu else None

        # If the user tries to access a menu that does not belong to them
        if user_menu_id and user_menu_id != menu.id:
            return HttpResponseForbidden("You are not allowed to view this menu.")
        
    if request.method == 'POST':
        if 'add_section' in request.POST:
            section_form = SectionForm(request.POST)
            if section_form.is_valid():
                new_section = section_form.save(commit=False)
                new_section.menu = menu
                new_section.save()
                return redirect('menu', id=id)  # Redirect to refresh the page
        elif 'add_food' in request.POST:
            food_form = FoodItemForm(request.POST)
            if food_form.is_valid():
                new_food = food_form.save(commit=False)
                section_id = request.POST.get('section_id')
                new_food.section = Section.objects.get(id=section_id)
                new_food.save()
                return redirect('menu', id=id)
        
    else:
        section_form = SectionForm()
        food_form = FoodItemForm()

    context = {
        'restaurant': restaurant,
        'menu': menu,
        'sections': sections,
        'section_form': section_form,
        'food_form': food_form,
        'user_menu_id': user_menu_id if user.is_authenticated and hasattr(user, 'restaurant_profile') else None

    }
    return render(request, 'menu.html', context)


@login_required(login_url='/login/')
def menuList(request):
    query = request.GET.get('query', '')
    sort_order = request.GET.get('sort', 'name_asc')
    page_number = request.GET.get('page', 1)

    menus = Menu.objects.filter(name__icontains=query) if query else Menu.objects.all()

    # Annotate each menu with the number of completed orders
    menus = menus.annotate(
        popularity=Count('restaurant__order', filter=Q(restaurant__order__status='completed'))
    )

    if sort_order == 'name_asc':
        menus = menus.order_by('name')
    elif sort_order == 'name_desc':
        menus = menus.order_by('-name')
    elif sort_order == 'popularity':
        menus = menus.order_by('-popularity')

    paginator = Paginator(menus, 8)  
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        menus = [{
            'name': menu.name,
            'id': menu.id,
            'image_url': menu.image.url if menu.image else None
        } for menu in page_obj]
        return JsonResponse({'menus': menus, 'has_next': page_obj.has_next()})
    
    return render(request, 'menu_list.html', {'page_obj': page_obj})

@login_required(login_url='/login/')
@require_POST
def delete_section(request):
    section_id = request.POST.get('section_id')
    menu_id = request.POST.get('menu_id')  # Retrieve the menu ID from the form
    if section_id:
        section = Section.objects.filter(id=section_id).first()
        if section:
            section.delete()
    return redirect('menu', id=menu_id)  # Use the retrieved menu ID for redirect

@login_required(login_url='/login/')
def edit_section(request):
    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        section_name = request.POST.get('name')
        section = get_object_or_404(Section, id=section_id)
        section.name = section_name
        section.save()
        return redirect('menu', id=section.menu.id)  # Redirect to the menu page
    return redirect('home')  # Fallback redirect if not a POST request

@login_required(login_url='/login/')
@require_POST
def add_section(request, menu_id):
    # Get the menu from the database
    menu = Menu.objects.get(id=menu_id)
    # Create a new section from POST data
    new_section_name = request.POST.get('name')
    Section.objects.create(menu=menu, name=new_section_name)
    # Redirect to the menu page 
    return redirect('menu', id=menu_id)

@login_required(login_url='/login/')
@require_POST
def add_food(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        FoodItem.objects.create(section=section, name=name, price=price)
        return redirect('menu', id=section.menu.id)  
    return render(request, 'add_food_form.html', {'section': section})  

@login_required(login_url='/login/')
@require_POST
def delete_food(request):
    food_id = request.POST.get('food_id')
    menu_id = request.POST.get('menu_id') 

    if food_id:
        food = FoodItem.objects.filter(id=food_id).first()
        if food:
            food.delete()

    return redirect('menu', id=menu_id) 

@login_required(login_url='/login/')
def edit_food(request):
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        food_item = get_object_or_404(FoodItem, pk=food_id)  
        food_item.name = request.POST.get('name', food_item.name) 
        food_item.price = request.POST.get('price', food_item.price)
        food_item.image = request.POST.get('image', food_item.image)

        
        food_item.save()
        # Since FoodItem is linked to Section, which is linked to Menu
        menu_id = food_item.section.menu.id  
        return redirect('menu', id=menu_id)  

    else:
        return HttpResponse("Invalid request", status=400)
    
@login_required
def add_to_cart(request, item_id):
    if request.method == 'POST':
        user = request.user
        food_item = get_object_or_404(FoodItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))  # Get quantity from POST data, default to 1 if not found


        cart = Order.objects.filter(customer=user, restaurant_id=food_item.section.menu.restaurant.id, status='cart').first()

        if not cart:
            # Create a new cart if not exists
            restaurant = get_object_or_404(RestaurantProfile, id=food_item.section.menu.restaurant.id)
            cart = Order.objects.create(customer=user, restaurant=restaurant, status='cart')

        order_item, created = OrderItem.objects.get_or_create(
            order=cart,
            food_item=food_item,
            defaults={'quantity': quantity}  # Start with provided quantity
        )

        if not created:
            # If the item is already in the cart, just increase the quantity
            order_item.quantity += quantity
            order_item.save()

        return redirect('cart_detail', cart_id=cart.id)  # Redirect to cart detail view
    
@login_required
def cart_detail(request, cart_id):
    user = request.user
    order = get_object_or_404(Order, id=cart_id, customer=user, status='cart')
    items = order.items.select_related('food_item__section__menu__restaurant')

    return render(request, 'cart.html', {'order': order, 'items': items})

@login_required
def adjust_item_quantity(request, item_id, action):
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user, order__status='cart')
    
    if action == 'increase':
        item.quantity += 1
        item.save()
        messages.success(request, "Item quantity increased.")
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            messages.success(request, "Item quantity decreased.")
        else:
            order_id = item.order.id
            item.delete()
            messages.success(request, "Item removed from cart because the quantity reached zero.")

    return redirect('cart_detail', cart_id=item.order.id)

@login_required
def cart_list(request):
    user = request.user
    carts = Order.objects.filter(customer=user, status='cart').select_related('restaurant__menu')
    menus = {cart.id: cart.restaurant.menu.name for cart in carts}  # Create a dictionary to store menu names keyed by order id
    return render(request, 'cart_list.html', {'carts': carts, 'menus': menus})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user, status='cart')
    order.delete()
    messages.success(request, "The order has been canceled successfully.")
    return redirect('cart_list') 

@require_POST
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    # Simulate payment process
    # Here we would have logic to handle the payment confirmation
    order.status = 'request'  # 'request' is the status after payment
    order.save()

    # Redirect to the order detail page after payment is confirmed
    return redirect('order_detail', order_id=order.id)

def order_confirmed(request, order_id):
    return render(request, 'cart_list.html', {'order_id': order_id})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'order_detail.html', {'order': order})

def restaurant_orders(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'restaurant_profile'):
        return redirect('login')

    restaurant = request.user.restaurant_profile
    orders_request = Order.objects.filter(restaurant=restaurant, status='request')
    orders_processing = Order.objects.filter(restaurant=restaurant, status='processing')
    orders_completed = Order.objects.filter(restaurant=restaurant, status='completed')

    # Count for each status
    orders_request_count = orders_request.count()
    orders_processing_count = orders_processing.count()
    orders_completed_count = orders_completed.count()

    context = {
        'orders_request': orders_request,
        'orders_processing': orders_processing,
        'orders_completed': orders_completed,
        'orders_request_count': orders_request_count,
        'orders_processing_count': orders_processing_count,
        'orders_completed_count': orders_completed_count,
    }
    return render(request, 'restaurant_orders.html', context)

@login_required
def restaurant_bookings(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'restaurant_profile'):
        return redirect('login')

    restaurant = request.user.restaurant_profile
    bookings_request = Booking.objects.filter(restaurant=restaurant, status='request').order_by('-date', '-time')
    bookings_accepted = Booking.objects.filter(restaurant=restaurant, status='accepted').order_by('-date', '-time')
    bookings_completed = Booking.objects.filter(restaurant=restaurant, status='completed').order_by('-date', '-time')

    # Count for each status
    bookings_request_count = bookings_request.count()
    bookings_accepted_count = bookings_accepted.count()
    bookings_completed_count = bookings_completed.count()

    context = {
        'bookings_request': bookings_request,
        'bookings_accepted': bookings_accepted,
        'bookings_completed': bookings_completed,
        'bookings_request_count': bookings_request_count,
        'bookings_accepted_count': bookings_accepted_count,
        'bookings_completed_count': bookings_completed_count,
    }
    return render(request, 'restaurant_bookings.html', context)



@require_POST
def update_order_status(request, order_id, new_status):
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()
    return redirect('restaurant_orders') 
@require_POST
def update_booking_status(request, booking_id, new_status):
    booking = Booking.objects.get(id=booking_id)
    booking.status = new_status
    booking.save()
    return redirect('restaurant_bookings') 

@login_required
def create_booking(request, restaurant_id):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.restaurant = get_object_or_404(RestaurantProfile, id=restaurant_id)
            booking.status = 'request'
            booking.save()
            return redirect('booking_details', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

@login_required
def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.customer != request.user:
        return HttpResponseForbidden()
    return render(request, 'booking_details.html', {'booking': booking})

@login_required
def menu_search(request):
    query = request.GET.get('query', '')
    if query:
        menus = Menu.objects.filter(name__icontains=query)  
        menus = Menu.objects.none()  

    return render(request, 'search_results.html', {'menus': menus})


@login_required(login_url='/login/')
@require_POST
def update_menu_name(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    new_name = request.POST.get('new_name')
    if new_name:
        menu.name = new_name
        menu.save()
    return redirect('menu', id=menu_id)  

@login_required
def restaurant_statistics(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'restaurant_profile'):
        return redirect('login')
    
    restaurant = request.user.restaurant_profile
    today = timezone.now().date()
    
    # Get today's and all time orders
    todays_orders = Order.objects.filter(restaurant=restaurant, created_at__date=today)
    all_orders = Order.objects.filter(restaurant=restaurant)
    
    # Calculate total sales for today and all time by summing manually
    todays_total_sales = sum(order.get_total_cost() for order in todays_orders)
    total_sales = sum(order.get_total_cost() for order in all_orders)
    
    # Calculate average order values
    todays_average_order_value = (todays_total_sales / todays_orders.count()) if todays_orders.exists() else 0
    average_order_value = (total_sales / all_orders.count()) if all_orders.exists() else 0
    
    # Count orders and bookings
    total_orders = all_orders.count()
    todays_orders_count = todays_orders.count()
    total_bookings = Booking.objects.filter(restaurant=restaurant).count()
    todays_bookings_count = Booking.objects.filter(restaurant=restaurant, date=today).count()

    # Calculate the most and least popular items
    item_sales = OrderItem.objects.filter(order__restaurant=restaurant).values(
        'food_item__name').annotate(total_sold=Count('quantity')).order_by('-total_sold')
    most_popular_items = item_sales[:1]
    least_popular_items = item_sales.reverse()[:1]

    todays_item_sales = OrderItem.objects.filter(
        order__restaurant=restaurant,
        order__created_at__date=today
    ).values('food_item__name').annotate(total_sold=Count('quantity')).order_by('-total_sold')
    todays_most_popular_items = todays_item_sales[:1]
    todays_least_popular_items = todays_item_sales.reverse()[:1]

    context = {
        'todays_total_sales': todays_total_sales,
        'todays_orders_count': todays_orders_count,
        'todays_average_order_value': todays_average_order_value,
        'todays_most_popular_items': todays_most_popular_items,
        'todays_least_popular_items': todays_least_popular_items,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'average_order_value': average_order_value,
        'total_bookings': total_bookings,
        'todays_bookings_count': todays_bookings_count,
        'most_popular_items': most_popular_items,
        'least_popular_items': least_popular_items
    }

    return render(request, 'restaurant_statistics.html', context)


@login_required(login_url='/login/')
def update_menu_image(request, id):
    menu = get_object_or_404(Menu, pk=id)

    if 'image' in request.FILES:
        menu.image = request.FILES['image']
        menu.save()
        return JsonResponse({'message': 'Image uploaded successfully'}, status=200)
    return JsonResponse({'message': 'No image provided'}, status=400)

@login_required
def upload_food_image(request):
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        food_item = get_object_or_404(FoodItem, pk=food_id)
        food_item.image = request.FILES.get('image')
        food_item.save()
        return JsonResponse({'message': 'Image uploaded successfully'}, status=200)
    return JsonResponse({'message': 'Failed to upload image'}, status=400)


