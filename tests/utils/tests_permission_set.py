'''
from django.test import TestCase
from org.custom_model_field import Permissions as PermissionSet
from collections import defaultdict


class PermissionSetTestCase(TestCase):
    "These testcases are for org.custom_model_field.PermissionSet class"

    def test_create_obj_with_zero(self):
        permission_int = 0
        permission_set = PermissionSet(permission_int)

        #Integer created by permission test and entered must be equal
        self.assertEqual(permission_int,permission_set.permissions_to_integer())

        # all permissions should be false when created with 0
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])


    def test_create_obj_with_permissions(self):
        # create a permission set obj for a random group (like executives)
        permission_int = 0
        permission_int |= 1 << PermissionSet.IS_STAFF               
        permission_int |= 1 << PermissionSet.CAN_REVIEW_PROOFS               
        permission_set = PermissionSet(permission_int)

        expected_result = permission_int
        actual_result = permission_set.permissions_to_integer()
        
        # integer created by permission test and entered must be equal
        self.assertEqual(actual_result, expected_result)
                
        # verify the set permissions 
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])

        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])


    def test_set_permission_with_empty_list(self):
        permission_list = []
        permission_set = PermissionSet()

        # verify the set permissions 
        self.assertFalse(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])


    def test_set_permission_with_list(self):
        permission_set = PermissionSet()
        permission_list = [PermissionSet.IS_STAFF, PermissionSet.CAN_REVIEW_PROOFS]
        permission_set.set_permissions(permission_list)

        # verify the set permissions 
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])

        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
    

    def test_permission_is_staff(self):
        # through set_permissions()
        permission_set = PermissionSet()
        permission_list = [PermissionSet.IS_STAFF]
        permission_set.set_permissions(permission_list)

        # verify the set permissions 
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])

        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])

        # through permission_int
        permission_int2 = 0
        permission_int2 |= 1 << PermissionSet.IS_STAFF               
        permission_set2 = PermissionSet(permission_int2)

        expected_result = permission_int2
        actual_result = permission_set.permissions_to_integer()
        
        # integer created by permission test and entered must be equal
        self.assertEqual(actual_result, expected_result)

        # verify the set permissions 
        self.assertTrue(permission_set2.permissions[PermissionSet.IS_STAFF])

        self.assertFalse(permission_set2.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(permission_set2.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set2.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set2.permissions[PermissionSet.CAN_CREATE_TASKS])


# todo: add tests for remaining permissions

'''