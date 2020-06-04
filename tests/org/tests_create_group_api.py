from org.models import *
from org.serializers import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase
from rest_framework import status
import json

class CreateGroupAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [post] /api/org/<org_id>/group/
    present in the view Org.views.GroupView.post 
    """

    create_group_api = '/api/org/1/group/'
    invalid_create_group_api='/api/org/12345/group/'
    valid_payload = {
        "name": "Test_Group", 
        "role": "Role hi Role", 
        "permissions_array": [0, 1, 2, 3, 4]
        }
    
    
    def setUp(self):
        """
            Create an organization in the test database
        """
        super(CreateGroupAPITestCase, self).setUp()
        create_org_data={
            'name': 'Ecell NITRR Open Source',
            'tagline': 'We love open source.'
        }
        serializer = CreateOrgSerializer(data = create_org_data)
        if serializer.is_valid():
            self.org = serializer.save()[0]

    def test_fail_without_auth_header(self):
        normal_client = self.create_normal_client()
        response = normal_client.post(self.create_group_api, json.dumps(self.valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_fail_invalid_org_id(self):
        auth_client = self.create_auth_client()
        response = auth_client.post(self.invalid_create_group_api,json.dumps(self.valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_not_a_member(self):
        auth_client = self.create_auth_client()
        response = auth_client.post(self.create_group_api,json.dumps(self.valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_without_input(self):
        auth_client = self.create_auth_client()

        # Creating an Admin member
        group = Group.objects.get(org=self.org, name='Admin')
        member= Member.objects.create(
            user = self.auth_user,
            group = group,
            org= self.org
        )
        response = auth_client.post(self.create_group_api,json.dumps({}),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_without_admin_permissions(self):
        auth_client = self.create_auth_client()

        # Creating an Volunteer member
        group = Group.objects.get(org=self.org, name='Volunteer')
        member= Member.objects.create(
            user = self.auth_user,
            group = group,
            org= self.org
        )
        response = auth_client.post(self.create_group_api,json.dumps(self.valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_with_correct_input(self):
        auth_client = self.create_auth_client()

        # Creating an Admin member
        group = Group.objects.get(org=self.org, name='Admin')
        Member.objects.create(
            user = self.auth_user,
            group = group,
            org= self.org
        )
        response = auth_client.post(self.create_group_api, json.dumps(self.valid_payload),
                                content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check db models
        created_group=Group.objects.get(org=self.org, name=self.valid_payload['name'])
        self.assertIsNotNone(created_group)
        self.assertIsNotNone(created_group.invite_slug)
        