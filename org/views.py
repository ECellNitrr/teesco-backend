from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from .serializers import *
from . import responses
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example


class OrgView(APIView):

    @swagger_auto_schema(
        operation_id='create_org',
        request_body=CreateOrgSerializer,
        responses={
            '201': set_example({}),
            '400': set_example(responses.create_org_400)
        },
    )
    def post(self,request):
        serializer = CreateOrgSerializer(data = request.data)

        if serializer.is_valid():
            # org = serializer.save()
            return Response({}, status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)