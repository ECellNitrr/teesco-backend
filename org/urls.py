from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', OrgView.as_view()),
    path('<int:org_id>/', EditOrgView.as_view(), name='edit_org'),
    path('<int:org_id>/volunteer/', AddVolunteer, name='add_volunteer'),
    path('<int:org_id>/group/', GroupView.as_view()),
    path('<int:org_id>/group/', GetGroup, name='get_group'),
    path(
        '<int:org_id>/group/<int:group_id>/',
        GroupDetailsView.as_view(),
        name='get_group_details'
    ),
]
