from rest_framework import status
from tests.AuthAPITestCase import AuthAPITestCase
from org.serializers import CreateOrgSerializer
from org.models import Group, Member
from tasks.models import Task

class CreateTaskAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [post] /api/tasks/org/<org_id>/
    present in the view Tasks.views.TaskView.post 
    """
    create_task_api = "/api/tasks/org/1"
    valid_payload = {
        "social_media_platform": "facebook",
        "share_type": "LINK",
        "share_link": "https://www.facebook.com/priyanshi417/posts/3092506014129036"
        }

    def setUp(self):
        """
            Create an organization in the test database
        """
        #Inheriting the base class functionality
        super(CreateTaskAPITestCase, self).setUp()
        # Create the org using serializer
        create_org_data = {
            'name': 'Ecell NITRR Open Source',
            'tagline': 'We love open source.'
        }
        serializer = CreateOrgSerializer(data=create_org_data)
        if serializer.is_valid():
            self.org = serializer.save()[0]

    def test_fail_without_auth_header(self):
        un_auth_client = self.create_normal_client()
        response = un_auth_client.post(self.create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_with_invalid_org(self):
        invalid_create_task_api = "/api/tasks/org/12345"
        auth_client = self.create_auth_client()
        response = auth_client.post(invalid_create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_with_invalid_member(self):
        auth_client = self.create_auth_client()
        response = auth_client.post(self.create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_unauthorised_member(self):
        auth_client = self.create_auth_client()

        # Creating Volunteer Member
        group = Group.objects.get(org=self.org, name='Volunteer')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )
        response = auth_client.post(self.create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_with_missing_share_link(self):
        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )

        # Payload with empty link
        invalid_payload = {
            "social_media_platform": "facebook", 
            "share_type": "LINK",
            "share_link": ""      
        }
        response = auth_client.post(self.create_task_api, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_missing_share_image(self):

        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )

        # Payload with empty IMAGE
        invalid_payload = {
            "social_media_platform": "whatsapp",
            "share_type": "IMG", 
            "share_img": ""
        }
        response = auth_client.post(self.create_task_api, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_missing_share_text(self):

        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )

        # Payload with empty TEXT
        invalid_payload = {
            "social_media_platform": "whatsapp",
            "share_type": "TEXT",
            "share_img": ""
        }

        response = auth_client.post(self.create_task_api, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_authorised_member(self):

        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )
        response = auth_client.post(self.create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check db models
        created_task =  Task.objects.get(
            org=self.org,
            social_media_platform=self.valid_payload['social_media_platform']
        )
        self.assertIsNotNone(created_task)
