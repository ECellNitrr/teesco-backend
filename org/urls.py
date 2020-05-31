from django.contrib import admin
from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', OrgView.as_view()),
    path('<int:org_id>/',EditOrg,name='edit_org'),
    path('<int:org_id>/volunteer/',AddVolunteer,name='add_volunteer'),
    path('<int:org_id>/group/',GetGroup,name='get_group'),
]