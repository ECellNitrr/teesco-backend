from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from org.custom_model_field import Permissions
from org.models import Org, Member
from .serializers import CreateTaskSerializer
from . import responses

# Create your views here.

class TaskView(APIView):

    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_id='get_task',
        responses={
            '200': set_example(responses.get_task_200),
            '404': set_example(responses.org_not_present_404),
            '401': set_example(responses.user_not_present_401),
            '403': set_example(responses.user_unauthorized_403),
            '400': set_example(responses.get_task_400)
        },
    )

    def get(self, request, org_id):
        try:
            org = Org.objects.get(pk=org_id)
        except Org.DoesNotExist:
            return Response(responses.org_not_present_404, status.HTTP_404_NOT_FOUND)

        # Check if the user is a member of the organisation
        try:
            member = Member.objects.get(
                user=request.user,
                org=org

            )
        except Member.DoesNotExist:
            return Response(responses.user_not_present_401, status.HTTP_401_UNAUTHORIZED)

        # Check if member is volunteer
        if member.group.name == 'Volunteer':
            response_object = []
            tasks = Task.objects.filter(org=org)
            for i in tasks:
                response_body = {
                    "task_id": i.id,
                    "author": i.author.username,
                    "social_media_platform": i.social_media_platform,
                    "description": i.description,
                    "share_type": i.share_type,
                    "share_link": i.share_link,
                    "share_text": i.share_text,
                    "share_img": request.build_absolute_uri(i.share_img.url) if i.share_img else None
                }
                response_object.append(response_body)
            return Response(response_object, status.HTTP_200_OK)
        else:
            return Response({"detail": "You are not authorised to view this."}, status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_id='create_task',
        request_body=CreateTaskSerializer,
        responses={
            '201': set_example({}),
            '404': set_example(responses.org_not_present_404),
            '401': set_example(responses.user_not_present_401),
            '403': set_example(responses.user_unauthorized_403),
            '400': set_example(responses.create_task_400)
        },
    )

    def post(self, request, org_id):
        '''This is to create Tasks by authorised members'''

        #Check if organisation exists
        try:
            org = Org.objects.get(pk=org_id)
        except Org.DoesNotExist:
            return Response(responses.org_not_present_404, status.HTTP_404_NOT_FOUND)

        #Check if the user is a member of the organisation
        try:
            member = Member.objects.get(
                user=request.user,
                org=org
            )
        except Member.DoesNotExist:
            return Response(responses.user_not_present_401, status.HTTP_401_UNAUTHORIZED)

        serializer = CreateTaskSerializer(data=request.data)

        #Check if member is STAFF and authorised to CREATE TASKS
        if member.group.perm_obj.permissions[Permissions.IS_STAFF] and \
            member.group.perm_obj.permissions[Permissions.CAN_CREATE_TASKS]:

            if serializer.is_valid():
                task = serializer.save(request.user, org)
                return Response({}, status.HTTP_201_CREATED)

            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)

        return Response(responses.user_unauthorized_403, status.HTTP_403_FORBIDDEN)
