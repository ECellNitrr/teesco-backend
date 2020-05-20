from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .models import *
from . import responses
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.swagger import set_example
from rest_framework.decorators import api_view, permission_classes
from org.custom_model_field import PermissionSet


class OrgView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='create_org',
        request_body=CreateOrgSerializer,
        responses={
            '201': set_example({}),
            '400': set_example(responses.create_org_400)
        },
    )
    def post(self,request):
        """
        1. when a Organisation is created Admin and Volunteer 
            groups are also automatically created for that org.
        2. Admin group has all the permissions available.
        3. Volunteer group has no permissions but when a user  
            joins that org without invite link he/she will be 
            put into volunteer group.
        4. The creator of the org will be automatically put into Admin group.
        """
        serializer = CreateOrgSerializer(data = request.data)

        if serializer.is_valid():
            # create org and default groups
            org,admin_group,admin_permission_set = serializer.save()

            # add creator to admin group
            member = Member.objects.create(
                user=request.user,
                org=org,
                group=admin_group,
                permissions=admin_permission_set
            )
            return Response({}, status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_id="list_permissions",
    method='GET',
    responses={
        '200': set_example({}),
        '400':set_example({"detail": "You are not authorised to view this."}),
        '401': set_example({"detail": "Authentication credentials were not provided."})
    }
)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_permissions_view(request):
    '''This function shall allow an ADMIN member to see the list of permissions'''
    
    members = Member.objects.filter(user=request.user)  # Receiving member status for the respective organisations
    for member in members:
        '''
        User might be a member of various organisations such
        that it isn't an ADMIN of all, so finding an organisation
        such that it is an ADMIN member, and printing permission
        dictionary if it happens to be one.
        '''                               
        if member.permissions.permissions.IS_ADMIN:     
            response_unit = member.permissions.permissions.get_permission_dict() 
            return Response(response_unit, status.HTTP_200_OK)
    
    '''
    If the user doesn't turn out to be an ADMIN at any organisation, or isn't a part of any
    it shall not be authorised to view permissions.
    '''
    return Response({"detail": "You are not authorised to view this."}, status.HTTP_400_BAD_REQUEST)
