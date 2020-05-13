from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from users.serializers import RegistrationSerializer
from . import responses

from drf_yasg.utils import swagger_auto_schema
from utils.response import set_example

class RegistrationView(APIView):

    @swagger_auto_schema(
        operation_id='create_user',
        request_body=RegistrationSerializer,
        responses={
            '201': set_example({}),
            '400': set_example(responses.user_registration_400)
        },
    )
    def post(self,request):
        serializer = RegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({}, status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)