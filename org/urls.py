from django.contrib import admin
from django.urls import path, include 
<<<<<<< HEAD

urlpatterns = [

=======
from .views import *

urlpatterns = [
    path('', OrgView.as_view()),
>>>>>>> upstream/dev
]