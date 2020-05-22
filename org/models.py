from django.db import models
from .custom_model_field import *
from users.models import User

# Create your models here.

class PermissionSetTestModel(models.Model):
    perm = PermissionField()

class Org (models.Model):
    route_slug = models.SlugField(max_length = 40, unique=True)
    can_join_without_invite = models.BooleanField(default = True)
    name = models.CharField(max_length=30, null=False, blank=False)
    tagline = models.CharField(max_length = 50)
    about = models.CharField(max_length = 500, null=True)
    profile_pic = models.ImageField(upload_to = 'uploads/org/profile_pic', null=True)
    cover_pic = models.ImageField(upload_to = 'uploads/org/cover_pic', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PermissionSet(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    org = models.ForeignKey(Org,on_delete=models.CASCADE)
    permissions = PermissionField()
    
    def __str__(self):
        return f'{self.id}-{self.permissions.permissions_to_integer()}'



class Group (models.Model):
    name = models.CharField(max_length = 30, null=False, blank=False)
    role = models.CharField(max_length = 200)
    invite_slug = models.SlugField(max_length = 40, unique=True)
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
        return f'{self.id}-{self.org.name}-{self.group.name}-{self.user.username}'


class Leaderboard (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    points = models.IntegerField()
    org = models.ForeignKey(Org,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}-{self.org.name}-{self.user.username}-{self.points}'