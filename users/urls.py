from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include 

urlpatterns = [

]
=======
from django.urls import path, include
from users.views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
>>>>>>> upstream/dev
