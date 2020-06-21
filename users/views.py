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
from rest_framework.parsers import MultiPartParser
from users.models import User
from org.models import *
from django.utils.crypto import get_random_string
from utils.email_service import send_email
from django.utils import timezone
import datetime


class RegistrationView(APIView):

    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_id='create_user',
        request_body=RegistrationSerializer,
        responses={
            '201': set_example(responses.user_registration_success_201),
            '400': set_example(responses.user_registration_400)
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(responses.user_registration_success_201, status.HTTP_201_CREATED)
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
                        return Response({'detail': 'Credentials did not match'}, status.HTTP_401_UNAUTHORIZED)
                    
                except User.DoesNotExist:
                    return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)     
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    @swagger_auto_schema(
        operation_id='forget_password',
        request_body=ForgetPasswordSerializer,
        responses={
            '200': set_example(responses.forget_password_200),
            '400': set_example(responses.forget_password_400),
            '404': set_example(responses.login_404),
        },
    )
    def post(self, request):
        """
        Forgot Password API where the email is posted and OTP is sent to the user.
        """
        
        serializer = ForgetPasswordSerializer(data=request.data)

        # Checking if the email entered is valid.
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Check if such a user exists.
            try:
                user = User.objects.get(email=valid_data['email'])
            except User.DoesNotExist:
                return Response(responses.login_404, status.HTTP_404_NOT_FOUND)
            else:
                # Setting Variables to check the time lapse.
                time_now = datetime.datetime.now()
                otp_created_at = user.otp_created_at
                one_hour = datetime.timedelta(hours = 1)

                # Mail Variables
                subject = 'OTP to Reset your Password'
                body = "Dear user,</br></br>\
                <b>The OTP to reset your password is {}</b>.</br>\
                Please do not share it with anyone.</br>\
                </br>\
                Best Regards,</br>\
                Teesco (Volunteer Management System)"

                # Check if OTP was ever generated for this user.
                if user.otp == None:
                    self.generate_otp(user)
                    send_email.delay([user.email], subject, body.format(user.otp))
                
                # Check if the time lapse is greater than 1 hour.
                elif time_now-otp_created_at.replace(tzinfo=None)>one_hour:
                    self.generate_otp(user)
                    send_email.delay([user.email], subject, body.format(user.otp))

                else:
                    send_email.delay([user.email], subject, body.format(user.otp))
                
                return Response(responses.forget_password_200, status.HTTP_200_OK)

        # If the email entered was invalid or empty.
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)
        
    def generate_otp(self, user):
        """
        Method to generate OTPs and save it in OTP field.
        """
        user.otp = get_random_string(5, allowed_chars='0123456789')
        user.otp_created_at = timezone.now()
        user.save()
               
        


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


@swagger_auto_schema(
    operation_id="list_orgs",
    method='get',
    responses={
        '200': set_example(responses.list_orgs_200),
        '401': set_example({"detail": "Authentication credentials were not provided."})
    }
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def list_orgs_view(request):
    """
    1. The API lists all the orgs the authorized user is a part of. 
    2. The API gives information about the orgs listed and 
    the group (user_role) the user is in. 
    3. It returns a null for profile pic if no picture url is found in that field.
    """
    members = Member.objects.filter(user=request.user)
    response_object = []
    for member in members:
        org = {
            'id': member.org.id,
            'org_name': member.org.name,
            'user_role': member.group.name,
            'profile_pic': request.build_absolute_uri(member.org.profile_pic.url) if member.org.profile_pic else None,
            'route_slug': member.org.route_slug,
            'tagline': member.org.tagline,
            'permissions' : {
                "Is Admin" : {
                    "value" : member.group.perm_obj.permissions[Permissions.IS_ADMIN],
                    "perm_int" : Permissions.IS_ADMIN
                },
                "Is Staff" : {
                    "value" : member.group.perm_obj.permissions[Permissions.IS_STAFF],
                    "perm_int" : Permissions.IS_STAFF
                },
                "Can Create Tasks" : {
                    "value" : member.group.perm_obj.permissions[Permissions.CAN_CREATE_TASKS],
                    "perm_int" : Permissions.CAN_CREATE_TASKS
                },
                "Can Reply to Queries" : {
                    "value" : member.group.perm_obj.permissions[Permissions.CAN_REPLY_TO_QUERIES],
                    "perm_int" : Permissions.CAN_REPLY_TO_QUERIES
                },
                "Can Review Proofs" : {
                    "value" : member.group.perm_obj.permissions[Permissions.CAN_REVIEW_PROOFS],
                    "perm_int" : Permissions.CAN_REVIEW_PROOFS
                },
            }
        }
        response_object.append(org)
    return Response(response_object, status.HTTP_200_OK)
