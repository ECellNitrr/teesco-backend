from django.test import TestCase
from org.custom_model_field import PermissionSet
from collections import defaultdict


class PermissionSetTestCase(TestCase):
    def test_create_with_empty_string(self):
        permission_int = 0
        permission_set = PermissionSet(permission_int)

        executive_permission_list = [ ]


        expected_result = executive_permission_list
        actual_result = PermissionSet.ret_permission_list(permission_int)

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)


        # all permissions should be false when the value is 0
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])

    def test_create_with_one_permission(self):
        permission_int = 2
        permission_set = PermissionSet(permission_int)

        executive_permission_list = [ 
            PermissionSet.IS_STAFF,
            ]


        expected_result = executive_permission_list
        actual_result = PermissionSet.ret_permission_list(permission_int)

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)

                
        # key with empty string should be false
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])

        # all permissions should be false when the value is 0
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])

    def test_create_with_two_permission(self):
        permission_int = 2+16
        permission_set = PermissionSet(permission_int)

        executive_permission_list = [ 
            PermissionSet.IS_STAFF,
            PermissionSet.CAN_REVIEW_PROOFS
            ]


        expected_result = sorted(executive_permission_list)
        actual_result = sorted(PermissionSet.ret_permission_list(permission_int))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)

                
        # key with empty string should be false
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])

        # all permissions should be false when the value is 0
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])

    def test_create_with_three_permission(self):
        permission_int = 2+16+4
        permission_set = PermissionSet(permission_int)

        executive_permission_list = [ 
            PermissionSet.IS_STAFF,
            PermissionSet.CAN_REVIEW_PROOFS,
            PermissionSet.CAN_CREATE_TASKS
            ]


        expected_result = sorted(executive_permission_list)
        actual_result = sorted(PermissionSet.ret_permission_list(permission_int))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)

                
        # key with empty string should be false
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])

        # all permissions should be false when the value is 0
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])

    def test_create_with_four_permission(self):
        permission_int = 2+16+4+8
        permission_set = PermissionSet(permission_int)

        executive_permission_list = [ 
            PermissionSet.IS_STAFF,
            PermissionSet.CAN_REVIEW_PROOFS,
            PermissionSet.CAN_CREATE_TASKS,
            PermissionSet.CAN_REPLY_TO_QUERIES
            ]


        expected_result = sorted(executive_permission_list)
        actual_result = sorted(PermissionSet.ret_permission_list(permission_int))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)

                
        # key with empty string should be false
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])

        # all permissions should be false when the value is 0
        self.assertFalse(permission_set.permissions[PermissionSet.IS_ADMIN])
        
    def test_create_with_all_permission(self):
        permission_int = 2+16+4+8+1
        permission_set = PermissionSet(permission_int)

        executive_permission_list = [ 
            PermissionSet.IS_STAFF,
            PermissionSet.CAN_REVIEW_PROOFS,
            PermissionSet.CAN_CREATE_TASKS,
            PermissionSet.CAN_REPLY_TO_QUERIES,
            PermissionSet.IS_ADMIN
            ]


        expected_result = sorted(executive_permission_list)
        actual_result = sorted(PermissionSet.ret_permission_list(permission_int))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)

                
        # key with empty string should be false
        self.assertTrue(permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertTrue(permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(permission_set.permissions[PermissionSet.IS_ADMIN])

        # all permissions should be false when the value is 0
        






    