from django.contrib import admin
from django.urls import path, include 
from account.views import custom_404_handler
from django.conf import settings
from django.conf.urls.static import static



handler404 = 'account.views.custom_404_handler'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('main.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

