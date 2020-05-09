from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import RegistrationSerializer

# Create your views here.

@api_view(['POST'])
def registrationview(request):

    serializer = RegistrationSerializer(data = request.data)
    data = {}
    if serializer.is_valid():
         user = serializer.save()
         data['success'] = True
         data['message'] = "Registration Successful"
    else:
        data = serializer.errors

    return Response(data)