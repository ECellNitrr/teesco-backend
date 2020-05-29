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

class GroupView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='create_group',
        request_body=CreateGroupSerializer,
        responses={
            '201': set_example({}),
            '400': set_example(responses.create_group_400),
            '401': set_example(responses.create_group_401),
            '403': set_example(responses.create_group_403),
            '404': set_example(responses.create_group_404)
        },
    )
    def post(self,request, org_id):
        """
        When a user posts the required details to this API, a number of checks follow:
        1. A check at the URL, that the org_id in the url exists or not(404).
        2. Whether the authorized user is a member of the organisation(401).
        3. Whether the authorzed member is an admin of the organisation(403).
        4. Whether the data posted is valid or not(400).
        5. If everything goes right, we create a unique route slug in the overidden save()
            which takes org_id as a parameter(201).
        """
        try:
            org = Org.objects.get(id=org_id)
        except:
            return Response({"message":"The organisation was not found"}, status.HTTP_404_NOT_FOUND)
        else:
            try:
                member = Member.objects.get(user = request.user, org= org)
            except:
                return Response({"detail":"You are not a member of this organisation"}, status.HTTP_401_UNAUTHORIZED)
            else:
                if member.permission_set.perm_obj.permissions[Permissions.IS_ADMIN]:
                    serializer = CreateGroupSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(org_id)
                        return Response({}, status.HTTP_201_CREATED)
                    else:
                        data = serializer.errors
                        return Response(data, status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"You do not have the required permissions."}, status.HTTP_403_FORBIDDEN)

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
