from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from users.models import User
from org.serializers import CreateOrgSerializer
from org.custom_model_field import PermissionField as Permissions
import uuid

class EditOrgTestCase(AuthAPITestCase):
    data_org_put = {
                "name":'test1',
                "tagline":'test1',
                "about":'test1'
        }
    data_org_put_empty = {
                "name":'',
                "tagline":'test1',
                "about":''
        }
    def setUp(self):
        #Inheriting the base class funtionality
        super(EditOrgTestCase,self).setUp()
        
        data_org = {
                "name":'test',
                "tagline":'test',
        }
        serializer = CreateOrgSerializer(data = data_org)
        if serializer.is_valid():
            self.org,self.admin_group,self.admin_permission_set = serializer.save()

    def test_fail_without_auth(self):
        add_volunteer_api = "/api/org/1/"
        un_auth_client = APIClient()
        response = un_auth_client.put(add_volunteer_api,data=self.data_org_put)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_with_not_admin(self):
        add_volunteer_api = "/api/org/1/"
        auth_client = self.create_auth_client()
        response = auth_client.put(add_volunteer_api,data=self.data_org_put)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_pass_with_admin(self):
        add_volunteer_api = "/api/org/1/"
        auth_client = self.create_auth_client()
        Member.objects.create(
            user=self.auth_user,
            org=self.org,
            group=self.admin_group,
            permission_set=self.admin_permission_set
        )
        response = auth_client.put(add_volunteer_api,data=self.data_org_put)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_with_unknown_org(self):
        add_volunteer_api = "/api/org/2/"
        auth_client = self.create_auth_client()
        response = auth_client.put(add_volunteer_api,data=self.data_org_put)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_empty_fields(self):
        add_volunteer_api = "/api/org/1/"
        auth_client = self.create_auth_client()
        Member.objects.create(
            user=self.auth_user,
            org=self.org,
            group=self.admin_group,
            permission_set=self.admin_permission_set
        )
        response = auth_client.put(add_volunteer_api,data=self.data_org_put_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.auth_user.delete()

