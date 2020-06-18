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

login_401 = {
    "detail": "Credentials did not match"
}

login_400 = {
    "email": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ]
}

login_404 = {
    "detail": "User not found"
}

login_202 = {
    "token": "Token 9935a8b04f2de7f5dec8f9e92a1893822b034dc7"
}

profile_200 = {
    'email': "user@host.com",
    'username': "username",
    'name': "name",
            'institution': "institution",
            'country_code': "country code",
            'phone': "phone number",
            'created_at': "time"
}

list_orgs_200 = [
    {
        "id": 1,
        "org_name": "E Cell",
        "user_role": "Admin",
        "profile_pic": "null",
        "route_slug": "0-e-cell",
        "tagline": "Leader Beyond Borders",
        "permissions": {
            "Is Admin": {
                "value": True,
                "perm_int": 1
            },
            "Is Staff": {
                "value": True,
                "perm_int": 4
            },
            "Can create tasks": {
                "value": True,
                "perm_int": 3
            },
            "Can create groups": {
                "value": True,
                "perm_int": 6
            },
            "Can reply to queries": {
                "value": True,
                "perm_int": 5
            }
        }
    },
    {
        "id": 2,
        "org_name": "NITRR",
        "user_role": "Admin",
        "profile_pic": "null",
        "route_slug": "2-nitrr",
        "tagline": "Work is worship",
        "permissions": {
            "Is Admin": {
                "value": True,
                "perm_int": 1
            },
            "Is Staff": {
                "value": True,
                "perm_int": 4
            },
            "Can create tasks": {
                "value": True,
                "perm_int": 3
            },
            "Can create groups": {
                "value": True,
                "perm_int": 6
            },
            "Can reply to queries": {
                "value": True,
                "perm_int": 5
            }
        }
    }
]

forget_password_200 = {
    'detail': 'An OTP has been sent to your email.'
}

forget_password_400 = {
  "email": [
    "Enter a valid email address.",
    "This field is required."
  ]
}

forget_password_404 = {
    'detail': 'User does not exist.'
}
