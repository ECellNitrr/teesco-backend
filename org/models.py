from django.db import models

# Create your models here.
from .custom_model_field import *

class Test(models.Model):
    perm = PermissionField()