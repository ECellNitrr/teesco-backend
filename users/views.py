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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from users.models import User




class RegistrationView(APIView):

    @swagger_auto_schema(
        operation_id='create_user',
        request_body=RegistrationSerializer,
        responses={
            '201': set_example({}),
            '400': set_example(responses.user_registration_400)
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

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
            '404': set_example(responses.login_404)
        },
    )



    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            found_email =  serializer.data['email']
            
            user = authenticate(
                username=serializer.data['email'],
                password=serializer.data['password']
                )     
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': f"Token {token.key}"}, status.HTTP_202_ACCEPTED)
            else:
                try:
                    if User.objects.get(email=found_email):
                        return Response({'message': 'Credentials did not match'}, status.HTTP_401_UNAUTHORIZED)
                    
                except User.DoesNotExist:
                    return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)     
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
                    
               
        


@swagger_auto_schema(
    operation_id="view_user",
    method='get',
    responses={
        '200': set_example(responses.profile_200),
        '401': set_example({"detail": "Authentication credentials were not provided."})
    }
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    user_object = {
        'email': user.email,
        'username': user.username,
        'name': user.name,
        'institution': user.institution,
        'country_code': user.country_code,
        'phone': user.phone,
        'created_at': user.created_at
    }
    return Response(user_object, status.HTTP_200_OK)
