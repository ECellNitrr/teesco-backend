from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from users.serializers import *
from django.contrib.auth import authenticate
from . import responses
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from rest_framework.authtoken.models import Token 


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
        """
            Registers a user with certain details into the database, after this users can log in.
        """
        serializer = RegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({}, status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @swagger_auto_schema(
        operation_id='login_user',
        request_body=LoginSerializer,
        responses={
            '202': set_example(responses.login_202),
            '400': set_example(responses.login_400),
            '401': set_example(responses.login_401),
        },
    )
    def post(self,request):
        """
            Logs in particular user with email and password, generates a token when logged in.
        """
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            user = authenticate(
                username= serializer.data['email'], 
                password= serializer.data['password']
            )
            
            if user:
                token,_ = Token.objects.get_or_create(user=user)

                return Response({
                    'token': f"Token {token.key}"
                }, status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'Credentials did not match'}, status.HTTP_401_UNAUTHORIZED)
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
