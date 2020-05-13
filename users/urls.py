from django.contrib import admin
from django.urls import path, include 
from users.views import RegistrationView

urlpatterns = [

    path('register/', RegistrationView, name = 'register')

]