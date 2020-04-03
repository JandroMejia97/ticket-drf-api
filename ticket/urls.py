"""ticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from rest_framework import routers

from apps.core.authentication import CustomAuthToken
from apps.tickets.urls import router as ticket_router

router = routers.DefaultRouter()
router.registry.extend(ticket_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('rest_framework.urls', 'drf_site'), namespace='drf_site')),
    path('api/', include((router.urls, 'ticket_api'), namespace='ticket_api')),
    path('api/auth/token/', CustomAuthToken.as_view()),
    path('', lambda request: redirect('api/', permanent=True))
]
