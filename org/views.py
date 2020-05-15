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
    when a org is created Admin and Volunteer
    groups are created automatically
    Generating permissions for that
    Voluntter group has no permissions
    """

        serializer = CreateOrgSerializer(data = request.data)

        if serializer.is_valid():
            org,admin_group,admin_permission_set = serializer.save()

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