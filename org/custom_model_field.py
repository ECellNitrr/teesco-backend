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

        self.permissions = defaultdict(int)
        permissions_array = permission_string.split(',')

        for permission in permissions_array:
            if len(permission) > 0:
                self.permissions[permission] = 1

    def set_permissions(self, permissions_array):
        """Revokes all the permissions and sets the permissions supplied in the array."""

        self.permissions = defaultdict(int)
        for permission in permissions_array:
            self.permissions[permission] = 1

    def to_binary(self):
        """Converts the permissions that are set(True) into binary number to be stored in the database."""

        permissions_array = []

        if self.permissions[self.IS_ADMIN] == 1:
            permissions_array.append(self.permissions[self.IS_ADMIN])
        if self.permissions[self.IS_ADMIN] != 1:
            permissions_array.append(0)

        if self.permissions[self.IS_STAFF] == 1:
            permissions_array.append(self.permissions[self.IS_STAFF])
        if self.permissions[self.IS_STAFF] != 1:
            permissions_array.append(0)

        if self.permissions[self.CAN_CREATE_TASKS] == 1:
            permissions_array.append(self.permissions[self.CAN_CREATE_TASKS])
        if self.permissions[self.CAN_CREATE_TASKS] != 1:
            permissions_array.append(0)

        if self.permissions[self.CAN_REPLY_TO_QUERIES] == 1:
            permissions_array.append(
                self.permissions[self.CAN_REPLY_TO_QUERIES])
        if self.permissions[self.CAN_REPLY_TO_QUERIES] != 1:
            permissions_array.append(0)

        if self.permissions[self.CAN_REVIEW_PROOFS] == 1:
            permissions_array.append(self.permissions[self.CAN_REVIEW_PROOFS])
        if self.permissions[self.CAN_REVIEW_PROOFS] != 1:
            permissions_array.append(0)

        permission_binary = map(str, permissions_array)
        permission_binary = ''.join(permission_binary)
        return permission_binary

    def __str__(self):
        self.to_binary()


class PermissionSetField(models.Model):
    """
    Custom model field to store permissions. Automatically converts db string to permission object
    and permission object into string to be stored in the database.
    """

    description = "To store and retrieve the permissions"
    perm = models.IntegerField(default=PermissionSet)

    def from_db_value(self, value, expression, connection, context):
        return PermissionSet(value)

    def to_python(self, value):
        return PermissionSet(value)

    def get_prep_value(self, value):
        if value:
            return value.to_binary()
        return ''

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
