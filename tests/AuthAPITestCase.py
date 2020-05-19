from rest_framework.test import APITestCase, APIClient
from users.models import User
from org.models import *
from org.custom_model_field import PermissionSet as Permissions
import uuid

class AuthAPITestCase(APITestCase):
    """
        Provides tools for testing authenticated API's
    """
    

    def setUp(self):
        """
        This provides basic setup needed to test an API which 
        needs authentication to be accessed.
        
        If setUp() is overridden in the child class then 
        super(childClass,self).setUp() should be called for 
        a proper setUp of AuthHelper class.
        """
        
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

        # create an un_authenticated user
        self.un_auth_user_email = "carbon.composite.dummy@gmail.com"
        self.un_auth_user_password = "belatrix.lestrange"
        self.un_auth_user = User.objects.create_user(
            email = self.un_auth_user_email,
            username = self.un_auth_user_email,
            name = "un auth user",
            password = self.un_auth_user_password,
            institution = 'NITRR',
            country_code = '+91',
            phone = '1234567890'
        ) 

        # create an authenticated user
        self.auth_user_email = "crash.test.dummy@gmail.com"
        self.auth_user_password = "test.modelx"
        self.auth_user = User.objects.create_user(
            email = self.auth_user_email,
            username = self.auth_user_email,
            name = "auth user",
            password = self.auth_user_password,
            institution = 'NITRR',
            country_code = '+91',
            phone = '1234567890'
        )

        # get auth token of auth_user
        login_payload = {
            'email' : self.auth_user_email,
            'password': self.auth_user_password
        }
        login_api = "/api/users/login/"
        client = APIClient()
        login_response = client.post(login_api, login_payload)
        self.auth_token = login_response.data['token'] 


    def create_auth_client(self):
        """
        This function returns a client with authorisation header set
        with the token of auth_user created in the setup() above.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.auth_token)
        return client


    def create_normal_client(self):
        """
        This function returns a client without auth headers.
        """
        client = APIClient()
        return client

    #Creates auth client in the org as volunteer
    def create_auth_client_in_org(self):
        """
        This function returns an authorized client.
        """
        login_api = "/api/users/login/"
        login_payload = {
            'email': self.auth_user_email,
            'password': self.auth_user_password
        }
        add_volunteer_api = "/api/org/1/volunteer/"
        auth_client = APIClient()
        login_response = auth_client.post(login_api, login_payload)
        auth_token = login_response.data['token']
        
        # Authorizing the requests by adding the token in header.
        auth_client.credentials(HTTP_AUTHORIZATION=auth_token)
        auth_client.get(add_volunteer_api)
        return auth_client

    def tearDown(self):
        """
        If tearDown() is overridden in the child class then 
        super(childClass,self).tearDown() should be called for 
        a proper teardown of AuthHelper class.
        """
        self.auth_user.delete()
        self.un_auth_user.delete()
