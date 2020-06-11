from rest_framework import serializers
from .models import Task


class CreateTaskSerializer(serializers.ModelSerializer):

    share_link = serializers.CharField(default=None)
    share_text = serializers.CharField(default=None)
    share_img = serializers.ImageField(default=None)

    class Meta:
        model = Task
        fields = [
            'social_media_platform', 'description', 'share_type', 'share_link', 'share_text', 'share_img']

    def save(self, user, org):

        valid_data = self.validated_data

        #Check for presence of Link if share type is link and then create respective task.
        if valid_data['share_type'] == 'LINK':
            if valid_data['share_link'] is None:
                raise serializers.ValidationError({'Share_Link':'Share link is required'})
            task = Task.objects.create(
                org=org,
                author=user,
                social_media_platform=valid_data['social_media_platform'],
                share_type=valid_data['share_type'],
                share_link=valid_data['share_link']
            )

        #Check for presence of Text if share type is text and then create respective task.
        elif valid_data['share_type'] == 'TEXT':
            if valid_data['share_text'] is None:
                raise serializers.ValidationError({'Share_text':'Share text is required'})
            task = Task.objects.create(
                org=org,
                author=user,
                social_media_platform=valid_data['social_media_platform'],
                share_type=valid_data['share_type'],
                share_text=valid_data['share_text']
            )

        #Check for presence of Image if share type is image and then create respective task.
        elif valid_data['share_type'] == 'IMG':
            if valid_data['share_img'] is None:
                raise serializers.ValidationError({'Share_img':'Share image is required'})
            task = Task.objects.create(
                org=org,
                author=user,
                social_media_platform=valid_data['social_media_platform'],
                share_type=valid_data['share_type'],
                share_img=valid_data['share_img']
            )

        return task
