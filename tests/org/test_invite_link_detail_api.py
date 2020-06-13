from rest_framework import status
from org.serializers import CreateOrgSerializer
from org.models import Group
from tests.AuthAPITestCase import AuthAPITestCase, APIClient

class InviteLinkDetailTestCase(AuthAPITestCase):
    '''
    This class tests the  API [get] /api/org/invite/<invite_slug>
    at Org.views.InviteLinkDetailView.get
    '''

    def setUp(self):
        """
            Create an organization in the test database
        """
        #Inheriting the base class functionality
        super(InviteLinkDetailTestCase, self).setUp()
        # Create the org using serializer
        data_org = {
            "name":'test',
            "tagline":'test'
        }
        serializer = CreateOrgSerializer(data=data_org)
        if serializer.is_valid():
            self.org = serializer.save()[0]


    def test_fail_invalid_invite_slug(self):
        un_auth_client = APIClient()
        response = un_auth_client.get("/api/org/invite/iamnotvalid")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pass_with_valid_invite_slug(self):
        un_auth_client = APIClient()
        volunteer_group = Group.objects.get(
            name='Volunteer',
            org=self.org,
        )
        response = un_auth_client.get("/api/org/invite/"+volunteer_group.invite_slug)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Checking values
        self.assertEqual(response.data['org_name'], volunteer_group.org.name)
        self.assertEqual(response.data['org_tagline'], volunteer_group.org.tagline)
        self.assertEqual(response.data['group_name'], volunteer_group.name)

        '''Used boolean for image as <ImageFieldFile: None> is
        different from None but yields desired behaviour here'''
        self.assertEqual(
            bool(response.data['org_profile_image']),
            bool(volunteer_group.org.profile_pic)
        )
