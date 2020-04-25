from django.db import models

# Create your models here.
from org.custom_model_field import *

class Test(models.Model):
    perm = PermissionSetField()
