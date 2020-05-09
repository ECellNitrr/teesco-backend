from django.contrib import admin
from django.urls import path, include 
from users.views import registrationview

urlpatterns = [

    path('register', registrationview, name = 'register')

]