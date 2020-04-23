from django.test import TestCase
from org.custom_model_field import PermissionSet


class PermissionSetTestCase(TestCase):
    def test_create_with_empty_string(self):
        empty_permission_set = PermissionSet()
                
        # key with empty string should be false
        self.assertFalse(empty_permission_set.permissions[''])
    

        # all permissions should be false when the string is empty
        self.assertFalse(empty_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertFalse(empty_permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(empty_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])



    def test_create_with_some_permissions(self):
        executive_permission_string = PermissionSet.CAN_REVIEW_PROOFS+','+ \
            PermissionSet.IS_STAFF+','+ PermissionSet.CAN_REPLY_TO_QUERIES

        executive_permission_set = PermissionSet(executive_permission_string) 


        # stringify function can place the permission in the string in any order
        # but we only care whether the permission is present or not. 
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(sorted(executive_permission_set.stringify().split(',')))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)


        # the permissions in the permission string should be true
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.IS_STAFF])


        # the permission not present in the string should be false
        self.assertFalse(executive_permission_set.permissions[PermissionSet.IS_ADMIN])



    def test_set_permissions(self):
        executive_permission_set = PermissionSet()
        executive_permission_list = [
            PermissionSet.CAN_REVIEW_PROOFS,
            PermissionSet.CAN_REPLY_TO_QUERIES,
            PermissionSet.IS_STAFF
        ]
        executive_permission_set.set_permissions(executive_permission_list)


        expected_result = list(sorted(executive_permission_list))
        actual_result = list(sorted(executive_permission_set.stringify().split(',')))


        #checking interconvertion between object and string
        self.assertListEqual(expected_result, actual_result)


        # the permissions in the permission string should be true
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.IS_STAFF])


        # the permission not present in the string should be false
        self.assertFalse(executive_permission_set.permissions[PermissionSet.IS_ADMIN])

    def test_create_with_some_permissions_two(self):
        executive_permission_string = PermissionSet.IS_ADMIN+','+ \
            PermissionSet.CAN_REVIEW_PROOFS

        executive_permission_set = PermissionSet(executive_permission_string) 


        # stringify function can place the permission in the string in any order
        # but we only care whether the permission is present or not. 
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(sorted(executive_permission_set.stringify().split(',')))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)


        # the permissions in the permission string should be true
        self.assertTrue(executive_permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        


        # the permission not present in the string should be false
        self.assertFalse(executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertFalse(executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(executive_permission_set.permissions[PermissionSet.IS_STAFF])


    def test_create_with_all_permissions(self):
        executive_permission_string = PermissionSet.IS_ADMIN+','+ \
                PermissionSet.CAN_REVIEW_PROOFS+','+ \
                PermissionSet.CAN_REPLY_TO_QUERIES+','+ \
                PermissionSet.CAN_CREATE_TASKS+','+ \
                PermissionSet.IS_STAFF


        executive_permission_set = PermissionSet(executive_permission_string) 


        # stringify function can place the permission in the string in any order
        # but we only care whether the permission is present or not. 
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(sorted(executive_permission_set.stringify().split(',')))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)


        # the permissions in the permission string should be true
        self.assertTrue(executive_permission_set.permissions[PermissionSet.IS_ADMIN])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.IS_STAFF])
        

        # key with empty string should be false
        self.assertFalse(executive_permission_set.permissions[''])


    def test_create_with_some_permissions_four(self):
        executive_permission_string = PermissionSet.CAN_REVIEW_PROOFS+','+ \
                PermissionSet.CAN_REPLY_TO_QUERIES+','+ \
                PermissionSet.CAN_CREATE_TASKS+','+ \
                PermissionSet.IS_STAFF
            

        executive_permission_set = PermissionSet(executive_permission_string) 


        # stringify function can place the permission in the string in any order
        # but we only care whether the permission is present or not. 
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(sorted(executive_permission_set.stringify().split(',')))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)


        # the permissions in the permission string should be true
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(executive_permission_set.permissions[PermissionSet.IS_STAFF])

        # the permission not present in the string should be false
        self.assertFalse(executive_permission_set.permissions[PermissionSet.IS_ADMIN])

    def test_create_with_some_permissions_one(self):
        executive_permission_string = PermissionSet.CAN_REVIEW_PROOFS

        executive_permission_set = PermissionSet(executive_permission_string) 


        # stringify function can place the permission in the string in any order
        # but we only care whether the permission is present or not. 
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(sorted(executive_permission_set.stringify().split(',')))

        # checking the interconvertion from string to object then to string 
        self.assertListEqual(expected_result, actual_result)


        # the permissions in the permission string should be true
        self.assertTrue(executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        


        # the permission not present in the string should be false
        self.assertFalse(executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertFalse(executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(executive_permission_set.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(executive_permission_set.permissions[PermissionSet.IS_ADMIN])

