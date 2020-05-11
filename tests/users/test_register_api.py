from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):

    def tests_registration(self):
        data = {"email" : "test@test.test","name" : "test","institution": "testing","password": "testingg","country_code": "+00","phone": "0000000000"}
        response = self.client.post("/api/users/register/", data)
        data = {"email" : "test@test.test","name" : "test","institution": "testing","password": "testingg","country_code": "+00","phone": "0000000000"}
        response = self.client.post("/api/users/register/", data)
        
        #self.assertEqual(response.status_code , status.HTTP_200_OK)
        
        print(response.data)
        '''
        self.assertEqual(response.data["email"] , "test@test.test")
        self.assertEqual(response.data["username"] , "test@test.test")
        self.assertEqual(response.data["name"] , "test")
        self.assertEqual(response.data["institution"] , "testing")
        self.assertEqual(response.data["country_code"] , "+00")
        self.assertEqual(response.data["phone"] , "0000000000")

        self.assertFalse(response.data["username"] , "test")
        '''