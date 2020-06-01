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
  "message":"You do not have the required permissions."
}

create_group_404={
  "message":"The organisation was not found"
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
