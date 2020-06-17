from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from users.models import User
from org.serializers import CreateOrgSerializer
from org.custom_model_field import Permissions
import uuid

class AvailablePermissionsAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [get] /api/org/org/available_permissions/
    present in the view Org.views.AvailablePermissionsView.get
    """

    availablePermissionsApiUrl = '/api/org/available_permissions/'
      
    def test_fail_without_auth_header(self):
        un_auth_client = APIClient()
        response = un_auth_client.get(self.availablePermissionsApiUrl)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_with_auth_header(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.availablePermissionsApiUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     