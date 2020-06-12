from org.models import *
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from org.serializers import *

class SearchOrgTestCase(AuthAPITestCase):
    """
    Testing the Search Org API
    """
    search_org_api='/api/org/'

    def setUp(self):
        """
            Create an organization in the test database
        """
        #Inheriting the base class functionality
        super(SearchOrgTestCase,self).setUp()
        # Create the org using serializer
        data_org = {
                "name":'Test_Org',
                "tagline":'testing is everything'
        }
        serializer = CreateOrgSerializer(data = data_org)
        if serializer.is_valid():
            self.org = serializer.save()[0]

    def test_fail_without_auth_header(self):
        un_auth_client = APIClient()
        response = un_auth_client.get(self.search_org_api)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_with_auth_header(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.search_org_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_with_all_orgs(self):
        """
        Testing if all the organizations are listed when 
        nothing is specified in search param.
        """
        auth_client = self.create_auth_client()
        all_orgs = ListOrgSerializer(Org.objects.all(), many=True)
        response = auth_client.get(self.search_org_api)
        self.assertEqual(response.data, all_orgs.data)

    def test_success_search_result(self):
        """
        Testing if only the organisation wanted ends
        up as a search result.
        """
        search_org_api = '/api/org/?search=test'
        auth_client = self.create_auth_client()
        filter_result = ListOrgSerializer(Org.objects.filter(name__startswith='test'), many=True)      
        response = auth_client.get(search_org_api)
        self.assertEqual(response.data, filter_result.data)


