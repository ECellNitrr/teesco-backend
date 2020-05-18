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
    operation_id="add_volunteer",
    operation_description="When an authenticated user hits this API it gets added to the volunteer group",
    method='get',
    responses={
        '200': set_example({"message": "You're added as a volunteer!"}),
        '401': set_example({"detail": "Authentication credentials were not provided."})
    }
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def AddVolunteer(request,org_id):
    org_count = Org.objects.filter(pk=org_id).count()
    if org_count>0:
        org = Org.objects.get(pk=org_id)
        volunteer_permissions = Permissions()
        volunteer_permission_set = PermissionSet.objects.get(
            name='Volunteer',
            org=org,
            permissions = volunteer_permissions,
        )
        volunteer_group = Group.objects.get(
            name='Volunteer',
            org=org,
            default_permission_set=volunteer_permission_set,
        )
        member = Member.objects.create(
            user = request.user,
            org = org,
            group = volunteer_group,
            permissions = volunteer_permission_set 
        )
        return Response({'You are added as a volunteer'},status.HTTP_201_CREATED)
    else:
        return Response({'Organization not present'},status.HTTP_400_BAD_REQUEST)
