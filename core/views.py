from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example


# Create your views here.
@swagger_auto_schema(
    operation_id="test_authentication",
    operation_description=
    """
        Checks if the user is authenticated or not.
    """,
    method='get',
    responses={
        '200': set_example({"message": "You are authenticated user!"}),
        '401': set_example({"detail": "Authentication credentials were not provided."})
    }
)
@api_view(['get'])
@permission_classes([IsAuthenticated])
def check_token_authentication(req):
    return Response({"message": "You are authenticated user!"}, status.HTTP_200_OK)