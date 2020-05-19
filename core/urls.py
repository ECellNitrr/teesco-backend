from django.contrib import admin
from django.urls import path, include 
from .views import *

urlpatterns = [
    path('check_auth/', check_token_authentication, name='check_auth'),
]