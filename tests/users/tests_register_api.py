from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):

    def tests_registration(self):
        data = {"email" : "test@test.test","name" : "test","institution": "testing","password": "testingg","country_code": "+00","phone": "0000000000"}
        response = self.client.post("/api/users/register/", data)
        
        self.assertEqual(response.data["success"] , True)
        self.assertEqual(response.data["message"] , 'Registration Successful')