from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path(
        '', 
        OrgView.as_view(),
        name='org_view'
    ),
    path(
        '<int:org_id>/volunteer/', 
        AddVolunteer, 
        name='add_volunteer'
    ),
    path(
        '<int:org_id>/group/', 
        GroupView.as_view(),
        name='group_view',
    ),
    path(
        '<int:org_id>/', 
        EditOrg, 
        name='edit_org'
    ),
    path(
        '<int:org_id>/profile_pic/', 
        UpdateProfilePic, 
        name='update_profile_pic'
    ),
    path(
        '<int:org_id>/group/<int:group_id>/',
        GroupDetailsView.as_view(),
        name='get_group_details'
    ),
    path(
        '<int:org_id>/group/<int:group_id>/members/',
        MembersListView.as_view(),
        name='group_members_list'

    ),
    path(
        'available_permissions/', 
        AvailablePermissionsView.as_view(), 
        name='available_permissions'
    ),
]
