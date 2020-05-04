from django.db import models

# Create your models here.
from .custom_model_field import *

class PermissionSetTestModel(models.Model):
    perm = PermissionField()

    def __str__(self):
        return f'{self.id}-{self.perm.permissions_to_integer()}'