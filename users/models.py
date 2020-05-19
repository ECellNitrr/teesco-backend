from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User (AbstractUser):
    route_slug = models.SlugField(max_length=40)
    email = models.EmailField(max_length=50)
<<<<<<< HEAD
    name = models.CharField(max_length=30)
    institution = models.CharField(max_length=30)
    country_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
=======
    name = models.CharField(max_length=30, null=False, blank=False)
    password = models.CharField(max_length = 30)
    username = models.CharField(max_length=30, null=False, blank=False, unique = True)
    institution = models.CharField(max_length=30,blank=True, null=True)
    country_code = models.CharField(max_length=6,blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
>>>>>>> upstream/dev

class Notification (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
<<<<<<< HEAD
        return self.user.name + self.id
=======
        return self.user.username + self.id
>>>>>>> upstream/dev
