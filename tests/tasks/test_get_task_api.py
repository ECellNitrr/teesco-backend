from org.serializers import CreateOrgSerializer
from tasks.serializers import CreateTaskSerializer
from tests.AuthAPITestCase import AuthAPITestCase
from org.models import Group, Member
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


class GetTasksAPITestCase(AuthAPITestCase):
    create_task_api = "/api/tasks/org/1"
    create_task_api_new = "/api/tasks/org/2"
    valid_payload = {
        "social_media_platform": "facebook",
        "description": "Test",
        "share_type": "LINK",
        "share_link": "https://www.facebook.com/ecellnitrr/photos/a.122992964426516/3044548662270917/?type=3&eid=ARATrXaYbYxtCq2dvU3p9k5tKogqQFcqdegbB6GrcyWGlnRz6MXiaiMm_aflnE9MLuvepFI4kiEy-Yoc&__tn__=EEHH-R"
    }
    def setUp(self):
        '''
        Creating an organization in test database
        '''
        super(GetTasksAPITestCase, self).setUp()
        # Create the org using serializer
        create_org_data = {
            'name': 'Ecell NITRR Open Source',
            'tagline': 'We love open source.'
        }
        serializer = CreateOrgSerializer(data=create_org_data)
        if serializer.is_valid():
            self.org = serializer.save()[0]

        user = User.objects.get(id=1)
        task_data = {
            "org": self.org,
            "author": user,
            "social_media_platform": "facebook",
            "description": "Test",
            "share_type": "LINK",
            "share_link": "https://www.facebook.com/ecellnitrr/photos/a.122992964426516/3044548662270917/?type=3&eid=ARATrXaYbYxtCq2dvU3p9k5tKogqQFcqdegbB6GrcyWGlnRz6MXiaiMm_aflnE9MLuvepFI4kiEy-Yoc&__tn__=EEHH-R"
        }
        task_data2 = {
            "org": self.org,
            "author": user,
            "social_media_platform": "facebook",
            "description": "Test",
            "share_type": "LINK",
            "share_link": "https://www.facebook.com/ecellnitrr/photos/a.122992964426516/3044548662270917/?type=3&eid=ARATrXaYbYxtCq2dvU3p9k5tKogqQFcqdegbB6GrcyWGlnRz6MXiaiMm_aflnE9MLuvepFI4kiEy-Yoc&__tn__=EEHH-R"
        }
        task_serializer1 = CreateTaskSerializer(data=task_data)
        if task_serializer1.is_valid():
            self.task = task_serializer1.save(user=user, org=self.org)

        task_serializer2 = CreateTaskSerializer(data=task_data2)
        if task_serializer2.is_valid():
            self.task = task_serializer2.save(user=user, org=self.org)

        data_org_new = {
            "name": 'test',
            "tagline": 'test'
        }
        serializer_new = CreateOrgSerializer(data=data_org_new)
        if serializer_new.is_valid():
            self.org_new = serializer_new.save()[0]

        task_data3 = {
            "org": self.org_new,
            "author": user,
            "social_media_platform": "facebook",
            "description": "Test",
            "share_type": "LINK",
            "share_link": "https://www.facebook.com/ecellnitrr/photos/a.122992964426516/3044548662270917/?type=3&eid=ARATrXaYbYxtCq2dvU3p9k5tKogqQFcqdegbB6GrcyWGlnRz6MXiaiMm_aflnE9MLuvepFI4kiEy-Yoc&__tn__=EEHH-R"
        }
        task_serializer3 = CreateTaskSerializer(data=task_data3)
        if task_serializer3.is_valid():
            self.task = task_serializer3.save(user=user, org=self.org_new)

    def test_fail_without_authheader(self):
        get_task_api = "/api/tasks/org/1"
        un_auth_client = APIClient()
        response = un_auth_client.get(get_task_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_invalid_org(self):
        get_task_api = "/api/tasks/org/3"
        auth_client = self.create_auth_client()
        response = auth_client.get(get_task_api)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_not_a_member(self):
        get_task_api = "/api/tasks/org/1"
        auth_client = self.create_auth_client()
        response = auth_client.get(get_task_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pass_authorized_member_singletask(self):
        get_task_api = "/api/tasks/org/2"
        auth_client = self.create_auth_client()
        volunteer_group = Group.objects.get(
            name='Volunteer',
            org=self.org_new,
        )
        member = Member.objects.create(
            user=self.auth_user,
            org=self.org_new,
            group = volunteer_group
        )
        response = auth_client.get(get_task_api)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pass_authorized_member_multitask(self):
        get_task_api = "/api/tasks/org/1"
        auth_client = self.create_auth_client()
        volunteer_group = Group.objects.get(
            name='Volunteer',
            org=self.org,
        )
        member = Member.objects.create(
            user=self.auth_user,
            org=self.org,
            group = volunteer_group
        )
        response = auth_client.get(get_task_api)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
