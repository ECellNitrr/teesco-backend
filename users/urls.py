from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('org/', list_orgs_view, name='list_orgs'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
]
