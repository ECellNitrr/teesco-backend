from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from users.models import User
from org.custom_model_field import PermissionSet as Permissions
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
        # Create the org
        self.org = Org.objects.create(
            route_slug= 'route_slug',
            name='test',
            tagline='test',
        )

        # Create default group permissions  
        self.volunteer_permissions = Permissions()
        
        #Create volunteer permission set objecct
        self.volunteer_permission_set = PermissionSet.objects.create(
            name = 'Volunteer',
            org = self.org,
            permissions = self.volunteer_permissions 
        )


        self.volunteer_group_invite_slug = str(self.org.id)+'-'+str(uuid.uuid4())

        #Create volunteer group with organization
        self.volunteer_group = Group.objects.create(
            name='Volunteer',
            role='''When a person clicks join org button of his own without a 
                invite link then he will be put into this group.''',
            invite_slug=self.volunteer_group_invite_slug,
            org=self.org,
            default_permission_set=self.volunteer_permission_set
        )
        
        #Create auth user object
        self.user_email = 'test@host.com'
        self.user_password = 'test_user.123'
        self.user = User.objects.create_user(
            email=self.user_email,
            username=self.user_email,
            name="test user",
            password=self.user_password,
            institution='E-Cell',
            country_code='+91',
            phone='5446465452'
        )
    
    def create_auth_client(self):
        """
        This function returns an authorized client.
        """
        login_api = "/api/users/login/"
        login_payload = {
            'email': self.user_email,
            'password': self.user_password
        }
        auth_client = APIClient()
        login_response = auth_client.post(login_api, login_payload)
        auth_token = login_response.data['token']

        # Authorizing the requests by adding the token in header.
        auth_client.credentials(HTTP_AUTHORIZATION=auth_token)
        return auth_client

    #Creates auth client in the org as volunteer
    def create_auth_client_in_org(self):
        """
        This function returns an authorized client.
        """
        login_api = "/api/users/login/"
        login_payload = {
            'email': self.user_email,
            'password': self.user_password
        }
        add_volunteer_api = "/api/org/1/volunteer/"
        auth_client = APIClient()
        login_response = auth_client.post(login_api, login_payload)
        auth_token = login_response.data['token']
        
        # Authorizing the requests by adding the token in header.
        auth_client.credentials(HTTP_AUTHORIZATION=auth_token)
        auth_client.get(add_volunteer_api)
        return auth_client
    
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
        auth_client = self.create_auth_client_in_org()
        response = auth_client.get(add_volunteer_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_bad_org_id(self):
        add_volunteer_api = "/api/org/2/volunteer/"
        auth_client = self.create_auth_client()
        response = auth_client.get(add_volunteer_api)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
 
    def tearDown(self):
        self.user.delete()
