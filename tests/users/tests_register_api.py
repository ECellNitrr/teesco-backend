from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class RegistrationTestCase(APITestCase):


    def test_registration_success_with_correct_credentials(self):
        data = {
            "email" : "test@test.test",
            "name" : "test",
            "institution": "testing",
            "password": "testingg",
            "country_code": "+00",
            "phone": "0000000000"
        }

        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)

        data_login = {

            "email" : "test@test.test",
            "password": "testingg"
        }

        response = self.client.post("/api/users/login/", data_login)
        self.assertEqual(response.status_code , status.HTTP_202_ACCEPTED)

    def test_registration_with_used_email(self):
        data = {
            "email" : "test@test.test",
            "name" : "test",
            "institution": "testing",
            "password": "testingg",
            "country_code": "+00",
            "phone": "0000000000"   
        }

        response = self.client.post("/api/users/register/", data)
        response = self.client.post("/api/users/register/", data)

        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_registration_without_optional_fields(self):
        data = {
            "email" : "test@test.test",
            "name" : "test",
            "password": "testingg",
        }

        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)


    def test_registration_without_email(self):
        data = {
            "name" : "test",
            "password": "testingg",
        }

        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_registration_without_name(self):
        data = {
            "email" : "test@test.test",
            "password": "testingg",
        }

        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_registration_without_password(self):
        data = {
            "email" : "test@test.test",
            "name" : "test",
        }

        response = self.client.post("/api/users/register/", data)

        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_email(self):
        data = {
            "email" : "testtest.test",
            "name" : "test",
            "password": "testingg",
        }

        response = self.client.post("/api/users/register/", data)

        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_registration_with_small_password(self):
        data = {
            "email" : "testtest.test",
            "name" : "test",
            "password": "te",
        }

        response = self.client.post("/api/users/register/", data)

        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)