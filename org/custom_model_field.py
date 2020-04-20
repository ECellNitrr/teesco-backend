from collections import defaultdict
from django.db import models


class PermissionSet:
    IS_ADMIN = 'IS_ADMIN'
    IS_STAFF = 'IS_STAFF'
    CAN_CREATE_TASKS = 'CAN_CREATE_TASKS'
    CAN_REPLY_TO_QUERIES = 'CAN_REPLY_TO_QUERIES'
    CAN_REVIEW_PROOFS = 'CAN_REVIEW_PROOFS'


    def __init__(self, permission_string=''):
        self.permissions = defaultdict(bool)
        permissions_array = permission_string.split(',')

        for permission in permissions_array:
            if len(permission)>0:
                self.permissions[permission] = True


    def set_permissions(self, permissions_array):
        self.permissions = defaultdict(bool)
        for permission in permissions_array:
            self.permissions[permission]=True


    def stringify(self):
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