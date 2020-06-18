from org.models import *
from org.serializers import UpdateProfilePicSerializer, CreateOrgSerializer
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class UpdateProfilePicAPITestCase(AuthAPITestCase):
    """
    This is to test the [put] /api/org/(org-id)/profile_pic/ 
    present in org.views.UpdateProfilePic update the organization logo.
    """

    update_profile_pic_api = '/api/org/1/profile_pic/'
    invalid_update_profile_pic_api = '/api/org/12345/profile_pic/'
    valid_image_path = 'assets/test/valid_pic.png'
    invalid_image_path = 'assets/test/invalid_pic.png'
    invalid_payload = {
        'profile_pic' : SimpleUploadedFile(
            'invalid_pic.png',
            content=open(invalid_image_path, 'rb').read()
        )
    }
    valid_payload = {
        'profile_pic' : SimpleUploadedFile(
            'valid_pic.png', 
            content=open(valid_image_path, 'rb').read()
        )
    }

    def setUp(self):
        """
            Create an organization in the test database
        """
        super(UpdateProfilePicAPITestCase, self).setUp()
        create_org_data={
            'name': 'Ecell NITRR Open Source',
            'tagline': 'We love open source.'
        }
        serializer = CreateOrgSerializer(data = create_org_data)
        if serializer.is_valid():
            self.org = serializer.save()[0]

    def test_fail_without_auth_header(self):
        normal_client = self.create_normal_client()
        response = normal_client.put(self.update_profile_pic_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_fail_invalid_org_id(self):
        auth_client = self.create_auth_client()
        response = auth_client.put(self.invalid_update_profile_pic_api)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_not_a_member(self):
        auth_client = self.create_auth_client()
        response = auth_client.put(self.update_profile_pic_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_without_admin_permissions(self):
        auth_client = self.create_auth_client()

        # Creating a Volunteer.
        group = Group.objects.get(org=self.org, name='Volunteer')
        member= Member.objects.create(
            user = self.auth_user,
            group = group,
            org= self.org
        )
        response = auth_client.put(self.update_profile_pic_api)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_with_invalid_pic(self):
        auth_client = self.create_auth_client()

        # Creating an Admin member
        group = Group.objects.get(org=self.org, name='Admin')
        Member.objects.create(
            user = self.auth_user,
            group = group,
            org= self.org
        )
        # Using an empty image as invalid pic.
        response = auth_client.put(self.update_profile_pic_api , self.invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_with_valid_pic(self):
        auth_client = self.create_auth_client()

        # Creating an Admin member
        group = Group.objects.get(org=self.org, name='Admin')
        Member.objects.create(
            user = self.auth_user,
            group = group,
            org= self.org
        )
        response = auth_client.put(self.update_profile_pic_api , self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deleting the uploaded image to clear up memory.
        os.remove('uploads/org/profile_pic/valid_pic.png')

    
        
