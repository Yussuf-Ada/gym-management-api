"""
URL configuration for gym_management project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('members.urls')),
    path('api/', include('memberships.urls')),
    path('api/', include('classes.urls')),
]
