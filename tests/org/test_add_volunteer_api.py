from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class AddVolunteerAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [get] /api/org/[org-id]/volunteer
    present in the view Org.views.AddVolunteer.get
    """
    

