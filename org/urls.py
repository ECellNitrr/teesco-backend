from django.contrib import admin
from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', OrgView.as_view()),
    path('<int:org_id>/volunteer/',AddVolunteer,name='add_volunteer'),
    path('<int:org_id>/permission_set/',Permission_Set_List, name = 'View Permission Set List'),
    path('<int:org_id>/group/', GroupView.as_view()),
]