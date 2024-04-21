from django.shortcuts import redirect
from django.urls import reverse
from main.views import *

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        exempt_urls = [reverse('login'), reverse('signup'), reverse('home')]  # Ensure these are the correct names used in your URLconf
        
        if not request.user.is_authenticated:
            if request.path not in exempt_urls:
                return redirect('signup')  

        return None
