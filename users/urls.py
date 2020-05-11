from django.contrib import admin
from django.urls import path, include 
from users.views import Registrationview

urlpatterns = [

    path('register/', Registrationview, name = 'register')

]