from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
            write_only=True,
            required=False,
            min_length=8,
            error_messages={
                "blank": "Password cannot be empty.",
                "min_length": "Password must be atleast 8 characters.",
            },
    )

    email = serializers.EmailField(validators=[
                UniqueValidator(
                    queryset=User.objects.all(),
                    message="This email is already registered with us.",
                )],
                error_messages = {
                    "required": "Email field is required.", 
                    "invalid" : "Kindly enter a Valid Email Address",
                })

    class Meta:
        model = User
        fields = ['email','name','password','institution','country_code','phone']
                extra_kwargs = {
                        "name": {"error_messages": {"required": "Name field is required."}}
                    }
         
        def save(self):

            user = User(
                email = self.validated_data['email'],
                username = self.validated_data['email'],
                name = self.validated_data['name'],
                password = self.validated_data['password'],
                institution = self.validated_data['institution'],
                country_code = self.validated_data['country_code'],
            )

            user.save()
            return user