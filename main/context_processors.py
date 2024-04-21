def menu_context(request):
    data = {}
    if request.user.is_authenticated:
        data['is_restaurant'] = hasattr(request.user, 'restaurant_profile')
        if data['is_restaurant']:
            data['menu_id'] = request.user.restaurant_profile.menu.id
    return data