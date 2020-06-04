from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.swagger import set_example
from org.custom_model_field import Permissions
from .serializers import *
from .models import *
from . import responses


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
    def post(self, request):
        """
        1. when a Organisation is created Admin and Volunteer
            groups are also automatically created for that org.
        2. Admin group has all the permissions available.
        3. Volunteer group has no permissions but when a user
            joins that org without invite link he/she will be
            put into volunteer group.
        4. The creator of the org will be automatically put into Admin group.
        """
        serializer = CreateOrgSerializer(data=request.data)

        if serializer.is_valid():
            # create org and default groups
            org, admin_group = serializer.save()

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
        When a user posts the required details to this API, a number of checks follow.
        If each of them pass, the group is created under the Organisation using the org_id.
        """
       
        try:
            org = Org.objects.get(id=org_id)
        except Org.DoesNotExist:
            # A check at the URL, that the org_id in the url exists or not(404).
            return Response(
                {"message":"The organisation was not found"}, 
                status.HTTP_404_NOT_FOUND
            )
        else:
            # Whether the authorized user is a member of the organisation(401).
            members = Member.objects.filter(user = request.user, org= org)
            if members.count()==0:
                return Response(
                    {"detail":"You are not a member of this organisation"}, 
                    status.HTTP_401_UNAUTHORIZED
                )
            else:
                # Whether the member is an Admin of the organisation.
                for member in members:
                    if member.group.perm_obj.permissions[Permissions.IS_ADMIN]:
                        serializer = CreateGroupSerializer(data=request.data)
                        if serializer.is_valid() and serializer.permissions_valid():
                            """
                            If everything goes right, we create a unique route slug
                            in the overidden save() which takes org_id as a parameter(201).
                            """
                            serializer.save(org_id)
                            return Response({}, status.HTTP_201_CREATED)
                        else:
                            # Whether the data posted is valid or not(400).
                            data = serializer.errors
                            return Response(data, status.HTTP_400_BAD_REQUEST)
                # If no member instance has Admin permission.
                return Response(
                    {"message":"You do not have the required permissions."}, 
                    status.HTTP_403_FORBIDDEN
                )


    @swagger_auto_schema(
    operation_id="get_groups_list",
    responses={
        '200': set_example(responses.get_group),
        '401': set_example(responses.user_unauthorized_401),
        '404': set_example({"detail": "This organisation doesn't exist."}),
        '400': set_example({"detail" : "You are not a member of this organisation"}),
        '403': set_example({"detail": "You are not authorised to view this."}),
        }
    )    
    def get(self, request, org_id):
        try:
            org = Org.objects.get(pk=org_id)
        except Org.DoesNotExist:
            return Response({"detail":"This organisation doesn't exist."}, status.HTTP_404_NOT_FOUND)
        
        try:
            member = Member.objects.get(
            user = request.user,
            org = org
            )
        except Member.DoesNotExist:
            return Response({"detail" : "You are not a member of this organisation"}, status.HTTP_400_BAD_REQUEST)
        
        if member.group.perm_obj.permissions[Permissions.IS_STAFF]:    
            groups = Group.objects.filter(org = org) 
            response_object = []
            for x in groups:
                memberLen = len(Member.objects.filter(group=x.id))
                response_object.append({"id":x.id, "name": x.name, "memberCount":memberLen})
                
            return Response(response_object,status.HTTP_200_OK)
        else :
            return Response({"detail": "You are not authorised to view this."}, status.HTTP_403_FORBIDDEN)
        
                
                

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
def AddVolunteer(request, org_id):
    org_count = Org.objects.filter(pk=org_id).count()

    if org_count > 0:
        org = Org.objects.get(pk=org_id)
        member_present = Member.objects.filter(
            user=request.user,
            org=org
        ).count()
        if member_present > 0:
            return Response({"message": "Already a member of the organization"}, status.HTTP_409_CONFLICT)
        else:

            volunteer_group = Group.objects.get(
                name='Volunteer',
                org=org,
            )
            member = Member.objects.create(
                user=request.user,
                org=org,
                group=volunteer_group,
            )
            return Response({"message": "You are added as a volunteer"}, status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Organization not present"}, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_id="edit_org",
    operation_description="When an authenticated user hits this API it gets added to the volunteer group",
    method='PUT',
    request_body=EditOrgSerializer,
    responses={
        '200': set_example(responses.update_org_200),
        '400': set_example(responses.org_not_present_400),
        '401': set_example(responses.user_unauthorized_401),
        '403': set_example(responses.admin_access_403),
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditOrg(request, org_id):
    user = request.user
    try:
        org = Org.objects.get(pk=org_id)
    except Org.DoesNotExist:
        return Response(responses.org_not_present_400, status.HTTP_400_BAD_REQUEST)

    try:
        member = Member.objects.get(user=user, org=org)
    except Member.DoesNotExist:
        return Response(responses.admin_access_403, status.HTTP_403_FORBIDDEN)

    isadmin = member.group.perm_obj.permissions_to_integer()
    # Checking if the isadmin is odd or even, if odd then the IS_ADMIN permission is enabled for the user
    if isadmin % 2 == 1:
        if request.method == "PUT":
            serializer = EditOrgSerializer(org, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(responses.update_org_200, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    else:
        return Response(responses.admin_access_403, status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(
    operation_id="get_groups_list",
    method='GET',
    responses={
        '200': set_example(responses.get_group),
        '401': set_example(responses.user_unauthorized_401),
        '404': set_example({"detail": "This organisation doesn't exist."}),
        '400': set_example({"detail": "You are not a member of this organisation"}),
        '403': set_example({"detail": "You are not authorised to view this."}),
    }
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def GetGroup(request, org_id):
    try:
        org = Org.objects.get(pk=org_id)
        print(org)
    except Org.DoesNotExist:
        return Response({"detail": "This organisation doesn't exist."}, status.HTTP_404_NOT_FOUND)

    try:
        member = Member.objects.get(
            user=request.user,
            org=org
        )
    except Member.DoesNotExist:
        return Response({"detail": "You are not a member of this organisation"}, status.HTTP_400_BAD_REQUEST)

    if member.group.perm_obj.permissions[Permissions.IS_STAFF]:
        group = Group.objects.all()
        response_object = []
        for x in group:
            memberLen = len(Member.objects.filter(group=x.id))
            response_object.append(
                {"id": x.id, "name": x.name, "memberCount": memberLen})

        return Response(response_object, status.HTTP_200_OK)
    else:
        return Response({"detail": "You are not authorised to view this."}, status.HTTP_403_FORBIDDEN)


class GroupDetailsView(APIView):
    '''
    This is to provide details of a particular
    group of an organisation to authorised
    members.
    '''

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='group_details',
        operation_description="Authenticated and permitted users receive\
         desired group details here",
        responses={
            '200': set_example(responses.group_details_200),
            '404': set_example(responses.org_not_present_404),
            '401': set_example(responses.user_not_present_401),
            '403': set_example(responses.user_unauthorized_403),
            '400': set_example(responses.group_not_present_400),
        },
    )

    def get(self, request, org_id, group_id):

        try:
            org = Org.objects.get(id=org_id)
        except Org.DoesNotExist:
            return Response(
                {"message":"This organisation does not exist"},
                status.HTTP_404_NOT_FOUND
            )

        try:
            group = Group.objects.get(
                id=group_id,
                org=org
            )
        except Group.DoesNotExist:
            return Response(
                {"message":"This group does not exist"},
                status.HTTP_400_BAD_REQUEST
            )

        try:
            member = Member.objects.get(
                user=request.user,
                org=org
            )
        except Member.DoesNotExist:
            return Response(
                {"detail":"You are not a member of this organisation"},
                status.HTTP_401_UNAUTHORIZED
            )
        
        if member.group.perm_obj.permissions[Permissions.IS_STAFF]:
            return Response(
                {
                    "id" : group_id,
                    "name" : group.name,
                    "role" : group.role,
                    "permissions" : {

                        "Is Admin":{
                            'value':  group.perm_obj.permissions[Permissions.IS_ADMIN],
                            'perm_int': Permissions.IS_ADMIN,
                        },
                        "Is Staff":{
                            'value': group.perm_obj.permissions[Permissions.IS_STAFF],
                            'perm_int': Permissions.IS_STAFF,
                        },
                        "Can create tasks":{
                            'value': group.perm_obj.permissions[Permissions.CAN_CREATE_TASKS],
                            'perm_int': Permissions.CAN_CREATE_TASKS,
                        },
                        "Can reply to queries":{
                            'value': group.perm_obj.permissions[Permissions.CAN_REPLY_TO_QUERIES],
                            'perm_int': Permissions.CAN_REPLY_TO_QUERIES,
                        },
                        "Can review proofs":{
                            'value':  group.perm_obj.permissions[Permissions.CAN_CREATE_TASKS],
                            'perm_int': Permissions.CAN_REVIEW_PROOFS,
                        }
                    }
                },
                status.HTTP_200_OK
            )
        return Response(
                    {"message":"You do not have the required permissions."},
                    status.HTTP_403_FORBIDDEN
                )