create_org_400 = {
    "name": [
        "This field may not be blank."
    ],
    "tagline": [
        "This field may not be blank."
    ]
}

add_volunteer_201 = {
    "detail": "You're added as a volunteer!"
}

org_not_present_400 = {
    "detail": "Organisation not present or many have been removed."
}

user_unauthorized_401 = {
    "detail": "Authentication credentials were not provided."
}

user_already_present_409 = {
    "detail": "Already a member of organization"
}

user_already_present_409 = {
    "detail": "Already a member of organization"
}

user_not_present_401 = {
    "detail":"You are not a member of this organisation"
}

update_org_200 = {
    "detail": "Organization details updated successfully"
}

admin_access_403 = {
    "detail": "You are not an admin of this organization"
}

empty_fields_500 = {
    "detail": "Can't update! one or more fields are empty!"
}

create_group_400={
  "name": [
    "This field is required.",
    "Ensure this field has no more than 30 characters."
  ],
  "role": [
    "This field is required.",
    "Ensure this field has no more than 200 characters."
  ],
  "permissions_array": [
    "This field is required.",
    "The permission ints in the array are not valid."
  ]
}

create_group_401={
  "detail": [
    "Authentication credentials were not provided.",
    "You are not a member of this organisation",
  ]
}

create_group_403={
  "detail":"You do not have the required permissions."
}

create_group_404={
  "detail":"The organisation was not found"
}

get_group = [
    {
        "id": 1,
        "name": "group1",
        "memberCount": 1
    },
    {
        "id": 2,
        "name": "group2",
        "memberCount": 3
    },
    {
        "id": 3,
        "name": "group3",
        "memberCount": 1
    }
]

org_not_present_404 = {
    "detail":"This organisation does not exist"
}

group_not_present_400 = {
    "detail":"This group does not exist"
}

user_unauthorized_403 = {
    "detail":"You do not have the required permissions."
}

group_details_200 = {
    "id": 1,
    "name": "head coordinator",
    "role": "Managing the sub-ordinates. Supervising and inteeractiong the respective domains.",
    "permissions": {
        "Is Admin":{
            'value':  False,
            'perm_int': 1,
        },
        "Is Staff":{
            'value': True,
            'perm_int': 4,
        },
        "Can create tasks":{
            'value': True,
            'perm_int': 3,
        },
        "Can create groups":{
            'value': True,
            'perm_int': 6,
        },
        "Can reply to queries":{
            'value':  False,
            'perm_int': 5,
        }
    }
}

members_list_200 = [
    
    {
        "id": 1,
        "name": "Sharanya Mehta",
        "profile_pic": "null",
    },
    {
        "id": 2,
        "name": "Nikita Saxena",
        "profile_pic": "null",
    }
]    
get_org_200 = {
        "id": 1,
        "route_slug": "slug",
        "can_join_without_invite": True,
        "name": "test",
        "tagline": "test",
        "about": "test",
        "profile_pic":  "null",
        "cover_pic":  "null"
} 
