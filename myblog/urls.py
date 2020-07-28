# mysite/urls.py

from django.contrib import admin
from django.urls import path

from blog import views  # Import the blog views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Set root to home view
]
