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

create_group_400={
  "name": [
    "Ensure this field has no more than 30 characters."
  ],
  "role": [
    "Ensure this field has no more than 200 characters."
  ],
  "default_permission_set": [
    "Invalid pk \"9\" - object does not exist."
  ]
}

create_group_401={
  "detail": [
    "Authentication credentials were not provided.",
    "You are not a member of this organisation",
  ]
}

create_group_403={
  "message":"You do not have the required permissions."
}

create_group_404={
  "message":"The organisation was not found"
}