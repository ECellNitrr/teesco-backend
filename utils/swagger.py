from drf_yasg.openapi import Response
from rest_framework import serializers 


# It will suffice in some cases (like error message to show the possible errors)
# This serialiser will be used for error messages
class PlaceholderSerialiser(serializers.Serializer):
    pass


# Used to create a example response object
def set_example(example, description='', schema=PlaceholderSerialiser):
    return Response(
        examples={"application/json": example},
        description=description, 
        schema=schema
    )