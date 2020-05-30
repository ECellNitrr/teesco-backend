from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from . import responses
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.swagger import set_example
from org.custom_model_field import Permissions


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
            org,admin_group = serializer.save()

            # add creator to admin group
            member = Member.objects.create(
                user=request.user,
                org=org,
                group=admin_group,
            )
            return Response({}, status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_id="add_volunteer",
    operation_description="When an authenticated user hits this API it gets added to the volunteer group",
    method='get',
    responses={
        '201': set_example(responses.add_volunteer_201),
        '400': set_example(responses.org_not_present_400),
        '401': set_example(responses.user_unauthorized_401),
        '409': set_example(responses.user_already_present_409)
    }
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def AddVolunteer(request,org_id):
    org_count = Org.objects.filter(pk=org_id).count()
    
    if org_count>0:
        org = Org.objects.get(pk=org_id)
        member_present = Member.objects.filter(
            user = request.user,
            org = org 
        ).count()
        if member_present>0:
            return Response({"message":"Already a member of the organization"},status.HTTP_409_CONFLICT)
        else:
            
            volunteer_group = Group.objects.get(
                name='Volunteer',
                org=org,
            )
            member = Member.objects.create(
                user = request.user,
                org = org,
                group = volunteer_group,
            )
            return Response({"message":"You are added as a volunteer"},status.HTTP_201_CREATED)
    else:
        return Response({"detail":"Organization not present"},status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    operation_id="edit_org",
    operation_description="When an authenticated user hits this API it gets added to the volunteer group",
    method='PUT',
    request_body = EditOrgSerializer,
    responses={
        '200': set_example(responses.update_org_200),
        '400': set_example(responses.org_not_present_400),
        '401': set_example(responses.user_unauthorized_401),
        '403': set_example(responses.admin_access_403),
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditOrg(request,org_id):
    org_count = Org.objects.filter(pk=org_id).count()
    if org_count>0:
        org = Org.objects.get(pk=org_id)
        user = request.user
        if Member.objects.filter(user=user,org=org).count()>0:
            isadmin = Member.objects.get(user=user,org=org).group.perm_obj.permissions_to_integer()
            #Checking if the isadmin is odd or even, if odd then the IS_ADMIN permission is enabled for the user
            if isadmin%2 == 1:
                if request.method == "PUT":
                    serializer = EditOrgSerializer(org,data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(responses.update_org_200,status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
            else:
                return Response(responses.admin_access_403,status.HTTP_403_FORBIDDEN)
        else:
            return Response(responses.admin_access_403,status.HTTP_403_FORBIDDEN)
    else:
            return Response(responses.org_not_present_400,status.HTTP_400_BAD_REQUEST)

