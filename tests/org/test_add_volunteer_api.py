from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from users.models import User
from org.serializers import CreateOrgSerializer
from org.custom_model_field import Permissions
import uuid
class AddVolunteerAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [get] /api/org/[org-id]/volunteer
    present in the view Org.views.AddVolunteer.get
    """
    def setUp(self):
        """
            Create an organization in the test database
        """
        #Inheriting the base class funtionality
        super(AddVolunteerAPITestCase,self).setUp()
        # Create the org using serializer
        data_org = {
                "name":'test',
                "tagline":'test'
        }
        serializer = CreateOrgSerializer(data = data_org)
        if serializer.is_valid():
            self.org = serializer.save()[0]
    

    
    def test_fail_without_auth_header(self):
        add_volunteer_api = "/api/org/1/volunteer/"
        un_auth_client = APIClient()
        response = un_auth_client.get(add_volunteer_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_with_auth_header(self):
        add_volunteer_api = "/api/org/1/volunteer/"
        auth_client = self.create_auth_client()
        response = auth_client.get(add_volunteer_api)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_already_member(self):
        add_volunteer_api = "/api/org/1/volunteer/"
        auth_client = self.create_auth_client()
        response = auth_client.get(add_volunteer_api)
        response = auth_client.get(add_volunteer_api)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_fail_bad_org_id(self):
        add_volunteer_api = "/api/org/2/volunteer/"
        auth_client = self.create_auth_client()
        response = auth_client.get(add_volunteer_api)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
 
    def tearDown(self):
        self.auth_user.delete()
