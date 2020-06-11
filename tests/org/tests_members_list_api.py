'''This module is to test members_list operation of the org app'''
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from org.models import *
from org.serializers import CreateOrgSerializer
from org.custom_model_field import Permissions

class MembersListAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [get] /api/org/(org-id)/group/(group-id)/members
    present in the class based view Org.views.MembersListView
    """

    def setUp(self):
        """
            Create an organization in the test database
        """
        #Inheriting the base class functionality
        super(MembersListAPITestCase, self).setUp()
        # Create the org using serializer
        data_org = {
            "name":'test',
            "tagline":'test'
        }
        serializer = CreateOrgSerializer(data=data_org)
        if serializer.is_valid():
            self.org = serializer.save()[0]

    def test_fail_without_auth_header(self):
        members_list_api = "/api/org/1/group/1/members/"
        un_auth_client = APIClient()
        response = un_auth_client.get(members_list_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_invalid_org(self):
        members_list_api = "/api/org/12345/group/1/members/"
        auth_client = self.create_auth_client()
        response = auth_client.get(members_list_api)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_invalid_group(self):
        members_list_api = "/api/org/1/group/12345/members/"
        auth_client = self.create_auth_client()
        response = auth_client.get(members_list_api)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_not_a_member(self):
        members_list_api = "/api/org/1/group/1/members/"
        auth_client = self.create_auth_client()
        response = auth_client.get(members_list_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_unauthorised_member(self):
        members_list_api = "/api/org/1/group/1/members/"
        auth_client = self.create_auth_client()
        volunteer_group = Group.objects.get(
            name='Volunteer',
            org=self.org,
        )
        member = Member.objects.create(
            user=self.auth_user,
            org=self.org,
            group=volunteer_group
        )
        response = auth_client.get(members_list_api)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_authorized_user(self):
        members_list_api = "/api/org/1/group/1/members/"
        auth_client = self.create_auth_client()
        admin_group = Group.objects.get(
            name='Admin',
            org=self.org,
        )
        member = Member.objects.create(
            user=self.auth_user,
            org=self.org,
            group=admin_group,
        )
        response = auth_client.get(members_list_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

