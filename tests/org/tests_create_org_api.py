from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class CreateOrgAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [post] /api/org/
    present in the view Org.views.OrgView.post 
    """
    create_org_api = '/api/org/'
    valid_payload = {
        'name': 'Ecell NITRR Open Source',
        'tagline': 'We do FOSS'
    }

    def test_fail_without_auth_header(self):
        normal_client = self.create_normal_client()
        response = normal_client.post(self.create_org_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_fail_without_input(self):
        auth_client = self.create_auth_client()
        response = auth_client.post(self.create_org_api,{})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_success_with_correct_input(self):
        auth_client = self.create_auth_client()
        response = auth_client.post(self.create_org_api, self.valid_payload)

        # check header
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check db models
        org = Org.objects.get(name=self.valid_payload['name'])
        admin_group=Group.objects.get(org=org, name='Admin')
        volunteer_group=Group.objects.get(org=org, name='Volunteer')
        member_obj = Member.objects.get(
            org=org,
            group=admin_group,
            user=self.auth_user
        )

        self.assertIsNotNone(org)
        self.assertIsNotNone(admin_group)
        self.assertIsNotNone(volunteer_group)
        self.assertIsNotNone(member_obj)
        