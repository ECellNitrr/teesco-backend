from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    route_slug = models.SlugField(max_length=40)
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=30, null=False, blank=False)
    profile_pic = models.ImageField(upload_to='uploads/user/profile_pic', null=True)
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=30, null=False, blank=False, unique=True)
    institution = models.CharField(max_length=30, blank=True, null=True)
    country_code = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.user.username + self.id)
