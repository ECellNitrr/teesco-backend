from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class ForgetPasswordTestCase(APITestCase):

    forget_password_api = '/api/users/forget_password/'

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = 'howsthetest'
        self.user = User.objects.create_user(
            email = self.email,
            username = self.email,
            name = "Test User",
            password = self.password,
            institution = 'NITRR',
            country_code = '+91',
            phone = '1234567890'
        )
    
    def test_fail_invalid_email(self):
        invalid_email_data = {
            'email' : 'invalid.email.com'
        }
        response = self.client.post(self.forget_password_api, invalid_email_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_unregistered_email(self):
        unregistered_email_data = {
            'email' :'user@example.com'
        }
        response = self.client.post(self.forget_password_api, unregistered_email_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success_valid_email(self):
        valid_email_data = {
            'email' :'test@gmail.com'
        }
        response = self.client.post(self.forget_password_api, valid_email_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def tearDown(self):
        self.user.delete()

