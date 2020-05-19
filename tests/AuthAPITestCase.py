from rest_framework.test import APITestCase, APIClient
from users.models import User
from org.models import *


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


    def tearDown(self):
        """
        If tearDown() is overridden in the child class then 
        super(childClass,self).tearDown() should be called for 
        a proper teardown of AuthHelper class.
        """
        self.auth_user.delete()
        self.un_auth_user.delete()
