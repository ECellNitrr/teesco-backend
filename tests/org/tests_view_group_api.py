'''This module is to test group_details operation of the org app'''
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from org.models import *
from org.serializers import CreateOrgSerializer
from org.custom_model_field import Permissions

class ViewGroupAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [get] /api/org/(org-id)/group/(group-id)/
    present in the class based view Org.views.GroupDetailsView
    """

    def setUp(self):
        """
            Create an organization in the test database
        """
        #Inheriting the base class functionality
        super(ViewGroupAPITestCase, self).setUp()
        # Create the org using serializer
        data_org = {
            "name":'test',
            "tagline":'test'
        }
        serializer = CreateOrgSerializer(data=data_org)
        if serializer.is_valid():
            self.org = serializer.save()[0]

    def test_fail_without_auth_header(self):
        group_detail_api = "/api/org/1/group/1/"
        un_auth_client = APIClient()
        response = un_auth_client.get(group_detail_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_invalid_org(self):
        group_detail_api = "/api/org/12345/group/1/"
        auth_client = self.create_auth_client()
        response = auth_client.get(group_detail_api)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_invalid_group(self):
        group_detail_api = "/api/org/1/group/12345/"
        auth_client = self.create_auth_client()
        response = auth_client.get(group_detail_api)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_not_a_member(self):
        group_detail_api = "/api/org/1/group/1/"
        auth_client = self.create_auth_client()
        response = auth_client.get(group_detail_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_unauthorised_member(self):
        group_detail_api = "/api/org/1/group/1/"
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
        response = auth_client.get(group_detail_api)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_authorized_user(self):
        group_detail_api = "/api/org/1/group/1/"
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
        response = auth_client.get(group_detail_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
