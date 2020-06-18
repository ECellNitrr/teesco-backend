from django.shortcuts import render
from rest_framework import status, generics, filters
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


class OrgView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    serializer_class = ListOrgSerializer
    queryset = Org.objects.all()
    filter_backends = [filters.SearchFilter]
    # Searching on the basis of two fields name and tagline.
    search_fields = ['name', 'tagline']


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

class OrgDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="edit_org",
        request_body=EditOrgSerializer,
        responses={
            '200': set_example(responses.update_org_200),
            '400': set_example(responses.org_not_present_400),
            '401': set_example(responses.user_unauthorized_401),
            '403': set_example(responses.admin_access_403),
        }
    )
    def put(self, request, org_id):
        user = request.user
        try:
            org = Org.objects.get(pk=org_id)
        except Org.DoesNotExist:
            return Response(responses.org_not_present_400, status.HTTP_400_BAD_REQUEST)

        try:
            member = Member.objects.get(user=user, org=org)
        except Member.DoesNotExist:
            return Response(responses.admin_access_403, status.HTTP_403_FORBIDDEN)

        if member.group.perm_obj.permissions[Permissions.IS_ADMIN]:
            serializer = EditOrgSerializer(org, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(responses.update_org_200, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(responses.admin_access_403, status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_id="get_org",
        responses={
            '200': set_example(responses.get_org_200),
            '400': set_example(responses.org_not_present_400),
            '401': set_example(responses.user_unauthorized_401),
        }
    )
    def get(self, request, org_id):
        user = request.user
        try:
            org = Org.objects.get(pk=org_id)
        except Org.DoesNotExist:
            return Response(responses.org_not_present_400, status.HTTP_400_BAD_REQUEST)

        response_body = {
            "id": org.id,
            "route_slug": org.route_slug,
            "can_join_without_invite": org.can_join_without_invite,
            "name": org.name,
            "tagline": org.tagline,
            "about": org.about,
            "profile_pic": org.profile_pic if org.profile_pic else None,
            "cover_pic": org.cover_pic if org.cover_pic else None
        }
        return Response(response_body, status.HTTP_200_OK)


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
                {"detail":"The organisation was not found"}, 
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
                    {"detail":"You do not have the required permissions."}, 
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
            return Response({"detail": "Already a member of the organization"}, status.HTTP_409_CONFLICT)
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
            return Response({"detail": "You are added as a volunteer"}, status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Organization not present"}, status.HTTP_400_BAD_REQUEST)



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
                {"detail":"This organisation does not exist"},
                status.HTTP_404_NOT_FOUND
            )

        try:
            group = Group.objects.get(
                id=group_id,
                org=org
            )
        except Group.DoesNotExist:
            return Response(
                {"detail":"This group does not exist"},
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
                    {"detail":"You do not have the required permissions."},
                    status.HTTP_403_FORBIDDEN
                )

class MembersListView(APIView):
    '''
    This is to provide the list of members
    present in a particular group of the 
    organisation to STAFF members.
    '''

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='get_members_list',
        operation_description="Authenticated and permitted users receive\
         desired group details here",
        responses={
            '200': set_example(responses.members_list_200),
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
                responses.org_not_present_404,
                status.HTTP_404_NOT_FOUND
            )

        try:
            group = Group.objects.get(
                id=group_id,
                org=org
            )
        except Group.DoesNotExist:
            return Response(
                responses.group_not_present_400,
                status.HTTP_400_BAD_REQUEST
            )

        try:
            member = Member.objects.get(
                user=request.user,
                org=org
            )
        except Member.DoesNotExist:
            return Response(
                responses.user_not_present_401,
                status.HTTP_401_UNAUTHORIZED
            )
        
        if member.group.perm_obj.permissions[Permissions.IS_STAFF]:
            response_object = []
            members = Member.objects.filter(
                org = org,
                group = group
            )
            for mem in members:
                mem_present = {
                    'id': mem.id,
                    'name': mem.user.name,
                    'profile_pic': request.build_absolute_uri(mem.user.profile_pic.url) if mem.user.profile_pic else None,
                }
                response_object.append(mem_present)
            return Response(response_object, status.HTTP_200_OK)
        return Response(
                    responses.user_unauthorized_403,
                    status.HTTP_403_FORBIDDEN
                )
