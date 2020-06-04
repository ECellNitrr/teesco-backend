create_org_400 = {
  "name": [
    "This field may not be blank."
  ],
  "tagline": [
    "This field may not be blank."
  ]
}

add_volunteer_201 = {
  "message": "You're added as a volunteer!"
}

org_not_present_400 = {
  "detail": "Organisation not present or many have been removed."
}

user_unauthorized_401 = {
  "detail": "Authentication credentials were not provided."
}

user_already_present_409 = {
  "message": "Already a member of organization"
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

admin_access_401 = {
  "detail":[
    "Authentication credentials were not provided.",
    "You are not a member of this organisation.",
  ]
}

org_perm_403 = {
  "message":"You do not have the required permissions"
}

org_not_found_404 = {
  "message":"The organisation does not found"
}

update_org_200 ={
  "message":"Organization details updated successfully"
}

admin_access_403 = {
    "message": "You are not an admin of this organization"
}

empty_fields_500 = {
    "message": "Can't update! one or more fields are empty!"
}
