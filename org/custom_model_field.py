


class PermissionSet:

    """Helps in interconversion of permissions into objects(for ease of use) and integers(for storage in db)."""

    # These mappings are to reduce the chance to misspell the permission name
    IS_ADMIN = 'IS_ADMIN'  # 0 position
    IS_STAFF = 'IS_STAFF'   # 1 position
    CAN_CREATE_TASKS = 'CAN_CREATE_TASKS'   # 2 Position    
    CAN_REPLY_TO_QUERIES = 'CAN_REPLY_TO_QUERIES'   # 3 Position
    CAN_REVIEW_PROOFS = 'CAN_REVIEW_PROOFS' #4 Position


    def __init__(self,permission_int=0):

        """Creates a permission set object from the permission integer."""

        self.permissions = defaultdict(bool)

        if permission_int&1:
            self.permissions[IS_ADMIN] = True   #2^0 = 1

        if permission_int&2:
            self.permissions[IS_STAFF] = True   #2^1 = 2
        
        if permission_int&4:
            self.permissions[CAN_CREATE_TASKS] = True   #2^2 = 4

        if permission_int&8:
            self.permissions[CAN_REPLY_TO_QUERIES] = True   #2^3 = 8

        if permission_int&16:
            self.permissions[CAN_REVIEW_PROOFS] = True   #2^4 = 16

    
    def set_permissions(self, permissions_array):
        """Revokes all the permissions and sets the permissions supplied in the array."""

        self.permissions = defaultdict(bool)
        for permission in permissions_array:
            self.permissions[permission]=True


    def integer_conver(self):
        """Converts the permissions that are set(True) into an integer to be stored in the database."""

        permission_integer = 0

        if self.permissions[self.IS_ADMIN]:
            permission_integer+=1

        if self.permissions[self.IS_STAFF]:
            permission_integer+=2

        if self.permissions[self.CAN_CREATE_TASKS]:
            permission_integer+=4

        if self.permissions[self.CAN_REPLY_TO_QUERIES]:
            permission_integer+=8

        if self.permissions[self.CAN_REVIEW_PROOFS]:
            permission_integer+=16

        return permission_integer

    def __str__(self):

        """Returns a string of elements"""

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




class PermissionField(models.IntegerField):
    description = "Saves permissions as integers but returns a Permission Set"

    def __init__(self, *args, **kwargs):
        """This inherits most defaults of CharField except for the below"""

        kwargs['default'] = PermissionSet()
        kwargs['serialize'] = False
        
        super(PermissionSetField, self).__init__(*args, **kwargs)


    def from_db_value(self, value, expression, connection, context):
        return PermissionSet(value)

    def to_python(self, value):
        return PermissionSet(value)

    def get_prep_value(self, value):
        if value:
            return value.integer_conver()
        return 0

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)