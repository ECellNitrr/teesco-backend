from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password must be atleast 8 characters.",
        }, 
        allow_blank=False,
        required=True
    )

    email = serializers.EmailField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="This email is already registered with us.",
        )],
        error_messages = {
            "required": "Email field is required.", 
            "invalid" : "Kindly enter a Valid Email Address",
        }, 
        allow_blank=False,
        required=True
    )

    name = serializers.CharField(
        allow_blank=False,
        required=True,
        error_messages = {
            "required": "Name field is required.", 
        },)
    institution = serializers.CharField(allow_blank=True, required=False)
    country_code = serializers.CharField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['email','name','password','institution','country_code','phone']
         

class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField(allow_blank=False)
    password= serializers.CharField(allow_blank=False)