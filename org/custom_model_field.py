from collections import defaultdict
from django.db import models


class PermissionSet:
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
            self.permissions[permission]=True


    def permissions_to_integer(self):
        """Converts the permissions that are set(True) into an integer to be stored in the database."""

        permission_integer = 0
        for permission in self.permissions:
            if self.permissions[permission]:
                permission_integer |= 1 << permission
        
        return permission_integer


    def get_permission_dict(self):
        """Returns a dictionary of permissions available"""

        permissions_dict = {
            'Admin Permission' : self.IS_ADMIN,
            'Staff Permission' : self.IS_STAFF,
            'Permission for task creation' : self.CAN_CREATE_TASKS,
            'Permission to resolve queries' : self.CAN_REPLY_TO_QUERIES,
            'Permission to review proofs' : self.CAN_REVIEW_PROOFS
        ]

        return permissions_dict


    def __str__(self):
        """Returns a string of elements"""

        permissions_array = [str(x) for x in self.permissions]
        permission_string = ','.join(permissions_array)
        return permission_string




class PermissionField(models.IntegerField):
    "Saves permissions as an integer in the DB and returns PermissionSet obj when queried"

    def __init__(self, *args, **kwargs):
        kwargs['default'] = PermissionSet()
        super().__init__(*args, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["default"]
        return name, path, args, kwargs


    def from_db_value(self, value, expression, connection):
        return self.to_python(value)


    def to_python(self, value):
        if isinstance(value, PermissionSet):
            return value
        
        if isinstance(value, str):
            return PermissionSet(int(value)) 

        if value is None:
            return PermissionSet()
        
        return PermissionSet(value)
    

    def get_prep_value(self, value, *args, **kwargs):
        return value.permissions_to_integer()