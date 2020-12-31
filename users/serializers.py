from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from slugify import slugify

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
        error_messages={
            "required": "Email field is required.",
            "invalid" : "Kindly enter a Valid Email Address",
        },
        allow_blank=False,
        required=True
    )

    name = serializers.CharField(
        allow_blank=False,
        required=True,
        error_messages={
            "required": "Name field is required.", 
        },)
    institution = serializers.CharField(allow_blank=True, required=False, default=None)
    country_code = serializers.CharField(allow_blank=True, required=False, default=None)
    phone = serializers.CharField(allow_blank=True, required=False, default=None)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'institution', 'country_code', 'phone']

    def save(self):
        last_user_id = 0
        if User.objects.count() > 0:
            last_user_id = User.objects.last().id + 1

        route_slug = str(last_user_id) + ' ' + self.validated_data['name']
        route_slug = slugify(route_slug, max_length=40)

        user = User.objects.create_user(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            name=self.validated_data['name'],
            password=self.validated_data['password'],
            institution=self.validated_data['institution'],
            country_code=self.validated_data['country_code'],
            phone=self.validated_data['phone'],
            route_slug=route_slug,
        )

        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
