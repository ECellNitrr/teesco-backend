from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator


class CreateOrgSerializer(serializers.Serializer):
    name= serializers.EmailField(allow_blank=False)
    tagline= serializers.CharField(allow_blank=False)
    profile_pic = serializers.ImageField()