from django.db import models

# Create your models here.
class User (models.Model):
    id = models.AutoField(primary_key=True)
    route_slug = models.SlugField(max_length=40)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    institution = models.CharField(max_length=30)
    country_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Notification (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
