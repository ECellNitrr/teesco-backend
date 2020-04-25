from collections import defaultdict
from django.db import models


class PermissionSet:
    """Helps in interconversion of permissions into objects(for ease of use) and strings(for storage in db)."""

    # These mappings are to reduce the chance to misspell the permission name
    IS_ADMIN = 'IS_ADMIN'
    IS_STAFF = 'IS_STAFF'
    CAN_CREATE_TASKS = 'CAN_CREATE_TASKS'
    CAN_REPLY_TO_QUERIES = 'CAN_REPLY_TO_QUERIES'
    CAN_REVIEW_PROOFS = 'CAN_REVIEW_PROOFS'


    def __init__(self, permission_string=''):
        """Creates a permission set object from a list of comma separated permission names string."""
        
        self.permissions = defaultdict(bool)
        permissions_array = permission_string.split(',')

        for permission in permissions_array:
            if len(permission)>0:
                self.permissions[permission] = True


    def set_permissions(self, permissions_array):
        """Revokes all the permissions and sets the permissions supplied in the array."""

        self.permissions = defaultdict(bool)
        for permission in permissions_array:
            self.permissions[permission]=True


    def stringify(self):
        """Converts the permissions that are set(True) into string to be stored in the database."""

        permissions_array = []

        if self.permissions[self.IS_ADMIN]:
            permissions_array.append(self.IS_ADMIN)

        if self.permissions[self.IS_STAFF]:
            permissions_array.append(self.IS_STAFF)

        if self.permissions[self.CAN_CREATE_TASKS]:
            permissions_array.append(self.CAN_CREATE_TASKS)

        if self.permissions[self.CAN_REPLY_TO_QUERIES]:
            permissions_array.append(self.CAN_REPLY_TO_QUERIES)

        if self.permissions[self.CAN_REVIEW_PROOFS]:
            permissions_array.append(self.CAN_REVIEW_PROOFS)

        permission_string = ','.join(permissions_array)
        return permission_string


    def __str__(self):
        self.stringify()


class PermissionSetField(models.Model):
    """
    Custom model field to store permissions. Automatically converts db string to permission object
    and permission object into string to be stored in the database.
    """
    
    description = "To store and retrieve the permissions"
    perm = models.CharField(max_length=8196,default=PermissionSet)   
    def from_db_value(self, value, expression, connection, context):
        return PermissionSet(value)

    def to_python(self, value):
        return PermissionSet(value)

    def get_prep_value(self, value):
        if value:
            return value.stringify()
        return ''

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)