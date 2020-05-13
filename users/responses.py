from rest_framework import serializers


user_registration_400 = {
  "email": [
    "Email field is required.",
    "This email is already registered with us.",
  ],
  "name": [
    "Name field is required."
  ],
  "password": [
    "This field is required.",
    "Password must be atleast 8 characters.",
  ],
  "institution": [
    "This field is required."
  ],
  "country_code": [
    "This field is required."
  ],
  "phone": [
    "This field is required."
  ]
}

