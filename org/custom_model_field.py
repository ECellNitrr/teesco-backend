from collections import defaultdict
from django.db import models

class PERMISSION_INT_INVALID(Exception): 
    pass


class Permissions:
    """Helps in interconversion of permissions into objects(for ease of use) and integers(for storage in db)."""


    # These mappings are to reduce the chance to misspell the permission name
    # enum is not used here because addicidentally changing the order corrupt the exisiting DB records 

    IS_ADMIN = 0
    IS_STAFF = 1
    CAN_CREATE_TASKS = 2    
    CAN_REPLY_TO_QUERIES = 3
    CAN_REVIEW_PROOFS = 4


    def __init__(self,permission_int=0):
        """Creates a permission set object from the permission integer."""

        self.permissions = defaultdict(bool)

        self.permissions[self.IS_ADMIN] = bool(permission_int & (1 << self.IS_ADMIN))   
        self.permissions[self.IS_STAFF] = bool(permission_int & (1 << self.IS_STAFF))   
        self.permissions[self.CAN_CREATE_TASKS] = bool(permission_int & (1 << self.CAN_CREATE_TASKS))   
        self.permissions[self.CAN_REPLY_TO_QUERIES] = bool(permission_int & (1 << self.CAN_REPLY_TO_QUERIES))   
        self.permissions[self.CAN_REVIEW_PROOFS] = bool(permission_int & (1 << self.CAN_REVIEW_PROOFS))   
    

    def set_permissions(self, permissions_array):
        """Revokes all the permissions and sets the permissions supplied in the array."""

        self.permissions = defaultdict(bool)
        for permission in permissions_array:
            if permission in self.get_permission_list():
                self.permissions[permission]=True
            else:
                raise PERMISSION_INT_INVALID("The permission ints in the array are not valid.")


    def permissions_to_integer(self):
        """Converts the permissions that are set(True) into an integer to be stored in the database."""

        permission_integer = 0
        for permission in self.permissions:
            if self.permissions[permission]:
                permission_integer |= 1 << permission
        
        return permission_integer


    def get_permission_list(self):
        """Returns a list of permissions available"""

        permissions_list = [
            self.IS_ADMIN,
            self.IS_STAFF,
            self.CAN_CREATE_TASKS,
            self.CAN_REPLY_TO_QUERIES,
            self.CAN_REVIEW_PROOFS
        ]

        return permissions_list


    @staticmethod
    def get_permission_dict():
        """Returns a dict of permissions available"""

        permissions_dict = {
            'Is Admin': Permissions.IS_ADMIN,
            'Is Staff': Permissions.IS_STAFF,
            'Can create tasks': Permissions.CAN_CREATE_TASKS,
            'Can reply to queries': Permissions.CAN_REPLY_TO_QUERIES,
            'Can review proofs': Permissions.CAN_REVIEW_PROOFS,
        }

        return permissions_dict


    def __str__(self):
        """Returns a string of elements"""

        permissions_array = [str(x) for x in self.permissions]
        permission_string = ','.join(permissions_array)
        return permission_string




class PermissionField(models.IntegerField):
    "Saves permissions as an integer in the DB and returns Permissions obj when queried"

    def __init__(self, *args, **kwargs):
        kwargs['default'] = Permissions()
        super().__init__(*args, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["default"]
        return name, path, args, kwargs


    def from_db_value(self, value, expression, connection):
        return self.to_python(value)


    def to_python(self, value):
        if isinstance(value, Permissions):
            return value
        
        if isinstance(value, str):
            return Permissions(int(value)) 

        if value is None:
            return Permissions()
        
        return Permissions(value)
    

    def get_prep_value(self, value, *args, **kwargs):
        return value.permissions_to_integer()