from django.db import models
from django.utils import timezone
from .custom_model_field import *
from users.models import User

# Create your models here.

class Org (models.Model):
    route_slug = models.SlugField(max_length = 40)
    can_join_without_invite = models.BooleanField(default = True)
    name = models.CharField(max_length=30)
    tagline = models.CharField(max_length = 50)
    about = models.CharField(max_length = 500)
    profile_pic = models.ImageField(upload_to = 'teesco-backend/static/profile_pic')
    cover_pic = models.ImageField(upload_to = 'teesco-backend/static/cover_pic')
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name

class PermissionSet(models.Model):
    org = models.ForeignKey(Org,on_delete=models.CASCADE)
    permissions = PermissionField()

    def __str__(self):
        return f'{self.id}-{self.perm.permissions_to_integer()}'



class Group (models.Model):
    name = models.CharField(max_length = 30)
    role = models.CharField(max_length = 200)
    invite_slug = models.SlugField(max_length = 40)
    org = models.ForeignKey(Org,on_delete=models.CASCADE)
    default_permission_set  = models.ForeignKey(PermissionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Member (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    org = models.ForeignKey(Org,on_delete=models.CASCADE)
    group  = models.ForeignKey(Group,on_delete=models.CASCADE)
    permissions  = models.ForeignKey(PermissionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + self.id


class Leaderboard (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    points = models.IntegerField()
    org = models.ForeignKey(Org,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + self.id
