from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


class ListOrgsTestCase(APITestCase):

    def setUp(self):
        """
        Create and authorized user in test database.
        """
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

    def test_fail_without_auth_header(self):
        list_orgs_api = "/api/users/org/"
        un_auth_client = APIClient()
        response = un_auth_client.get(list_orgs_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_with_auth_header(self):
        list_orgs_api = "/api/users/org/"
        auth_client = self.create_auth_client()
        response = auth_client.get(list_orgs_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()
