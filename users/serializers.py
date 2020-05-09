from rest_framework import serializers
from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):

     class Meta:
        model = User
        fields = ['email','name','institution','country_code','phone']
         
         
        def save(self):
            user = User(
                email = self.validated_data['email'],
                username = self.validated_data['email'],
                name = self.validated_data['name'],
                institution = self.validated_data['institution'],
                country_code = self.validated_data['country_code'],
            )

            user.save()
            return user