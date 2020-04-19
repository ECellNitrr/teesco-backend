from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/query/',include('query.urls')),
    path('api/users/',include('users.urls')),
    path('api/org/',include('org.urls')),
]