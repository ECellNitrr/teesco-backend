from django.contrib import admin
from django.urls import path, include 
from users.views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
]