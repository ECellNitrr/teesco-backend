from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from org.serializers import CreateOrgSerializer
from org.custom_model_field import PermissionField as Permissions
import uuid


class GetOrgAPITestCase(AuthAPITestCase):
    def setUp(self):
        # Inheriting the base class funtionality
        super(GetOrgAPITestCase, self).setUp()

        data_org = {
            "name": 'test',
            "tagline": 'test',
        }
        serializer = CreateOrgSerializer(data=data_org)
        if serializer.is_valid():
            self.org, self.admin_group = serializer.save()

    def test_fail_without_auth(self):
        get_org_api = "/api/org/1/"
        un_auth_client = APIClient()
        response = un_auth_client.get(get_org_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_with_unknown_org(self):
        get_org_api = "/api/org/123123/"
        auth_client = self.create_auth_client()
        response = auth_client.get(get_org_api)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pass_with_auth_user(self):
        get_org_api = "/api/org/1/"
        auth_client = self.create_auth_client()
        response = auth_client.get(get_org_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        super(GetOrgAPITestCase,self).tearDown() 
