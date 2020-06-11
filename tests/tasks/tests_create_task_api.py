import uuid
from rest_framework import status
from tests.AuthAPITestCase import AuthAPITestCase
from org.serializers import CreateOrgSerializer, CreateGroupSerializer
from org.models import Group, Member
from tasks.models import Task
from org.custom_model_field import Permissions

class CreateTaskAPITestCase(AuthAPITestCase):
    """
    This class is to test the API [post] /api/tasks/org/<org_id>/
    present in the view Tasks.views.TaskView.post
    """
    create_task_api = "/api/tasks/org/1"
    valid_payload = {
        "social_media_platform": "facebook",
        "description": "Test",
        "share_type": "LINK",
        "share_link": "https://www.facebook.com/ecellnitrr/photos/a.122992964426516/3044548662270917/?type=3&eid=ARATrXaYbYxtCq2dvU3p9k5tKogqQFcqdegbB6GrcyWGlnRz6MXiaiMm_aflnE9MLuvepFI4kiEy-Yoc&__tn__=EEHH-R"
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

    def test_fail_without_can_create_task_permission(self):
        auth_client = self.create_auth_client()

        #Creating group without CAN_CREATE_TASK permission
        no_task_creation_permission = Permissions()
        no_task_creation_permission.set_permissions([
            Permissions.IS_ADMIN,
            Permissions.IS_STAFF,
            Permissions.CAN_REPLY_TO_QUERIES,
            Permissions.CAN_REVIEW_PROOFS,
        ])
        no_task_creation_invite_slug = str(1)+'-'+str(uuid.uuid4())
        no_task_creation_group = Group.objects.create(
            name='No Task creation',
            role='''This group is supposed to not possess permissions
                    necessary for creating tasks''',
            invite_slug=no_task_creation_invite_slug,
            org=self.org,
            perm_obj=no_task_creation_permission
        )

        #Making member of the group just created
        member = Member.objects.create(
            user=self.auth_user,
            group=no_task_creation_group,
            org=self.org
        )

        response = auth_client.post(self.create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_fail_without_staff_permission(self):
        auth_client = self.create_auth_client()

        #Creating group without STAFF permission
        not_staff_permission = Permissions()
        not_staff_permission.set_permissions([
            Permissions.IS_ADMIN,
            Permissions.CAN_CREATE_TASKS,
            Permissions.CAN_REPLY_TO_QUERIES,
            Permissions.CAN_REVIEW_PROOFS,
        ])
        not_staff_invite_slug = str(1)+'-'+str(uuid.uuid4())
        not_staff_group = Group.objects.create(
            name='Not Staff',
            role='This group is supposed to not possess staff permissions',
            invite_slug=not_staff_invite_slug,
            org=self.org,
            perm_obj=not_staff_permission
        )

        #Making member of the group just created
        member = Member.objects.create(
            user=self.auth_user,
            group=not_staff_group,
            org=self.org
        )

        response = auth_client.post(self.create_task_api, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_empty_input(self):
        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )

        empty_payload = {}

        response = auth_client.post(self.create_task_api, empty_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_invalid_share_type(self):
        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )

        # Payload with INVALID share_type
        invalid_payload = {
            "social_media_platform": "facebook",
            "description": "Test",
            "share_type": "INVALID",
            "share_link": "..."
        }
        response = auth_client.post(self.create_task_api, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_invalid_platform(self):
        auth_client = self.create_auth_client()

        # Creating Admin Member
        group = Group.objects.get(org=self.org, name='Admin')
        member = Member.objects.create(
            user=self.auth_user,
            group=group,
            org=self.org
        )

        # Payload with INVALID social_media_platform
        invalid_payload = {
            "social_media_platform": "INVALID",
            "description": "Test",
            "share_type": "LINK",
            "share_link": "..."
        }
        response = auth_client.post(self.create_task_api, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            "description": "Test",
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
            "description": "Test",
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
            "description": "Test",
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
        created_task = Task.objects.get(
            org=self.org,
            social_media_platform=self.valid_payload['social_media_platform']
        )
        self.assertIsNotNone(created_task)
