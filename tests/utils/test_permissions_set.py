from django.test import TestCase
from org.custom_model_field import PermissionSet


class PermissionSetTestCase(TestCase):
    def test_create_with_empty_string(self):
        empty_permission_set = PermissionSet()

        # key with empty string should be false
        self.assertEqual(empty_permission_set.permissions[''], 0)

        # all permissions should be false when the string is empty
        self.assertEqual(
            empty_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 0)
        self.assertEqual(
            empty_permission_set.permissions[PermissionSet.IS_ADMIN], 0)
        self.assertEqual(
            empty_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 0)

    def test_create_with_some_permissions(self):
        executive_permission_string = PermissionSet.CAN_REVIEW_PROOFS+',' + \
            PermissionSet.IS_STAFF+',' + PermissionSet.CAN_REPLY_TO_QUERIES

        executive_permission_set = PermissionSet(executive_permission_string)
        # print(executive_permission_set)

        # to_binary function can place the permission in the string in any order
        # but we only care whether the permission is present or not.
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(
            sorted(map(int, executive_permission_set.to_binary())))

        # checking the interconvertion from string to object then to string
        #self.assertListEqual(expected_result, actual_result)

        # the permissions in the permission string should be true
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_STAFF], 1)

        # the permission not present in the string should be false
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_ADMIN], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS], 0)

    def test_set_permissions(self):
        executive_permission_set = PermissionSet()
        executive_permission_list = [
            PermissionSet.CAN_REVIEW_PROOFS,
            PermissionSet.CAN_REPLY_TO_QUERIES,
            PermissionSet.IS_STAFF
        ]
        executive_permission_set.set_permissions(executive_permission_list)

        expected_result = list(sorted(executive_permission_list))
        actual_result = list(
            sorted(map(int, executive_permission_set.to_binary())))

        # the permissions in the permission string should be true
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_STAFF], 1)

        # the permission not present in the string should be false
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_ADMIN], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS], 0)

    def test_create_with_some_permissions_two(self):
        executive_permission_string = PermissionSet.IS_ADMIN+',' + \
            PermissionSet.CAN_REVIEW_PROOFS

        executive_permission_set = PermissionSet(executive_permission_string)

        # to_binary function can place the permission in the string in any order
        # but we only care whether the permission is present or not.
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(
            sorted(map(int, executive_permission_set.to_binary())))

        # the permissions in the permission string should be true
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_ADMIN], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 1)

        # the permission not present in the string should be false
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_STAFF], 0)

    def test_create_with_all_permissions(self):
        executive_permission_string = PermissionSet.IS_ADMIN+',' + \
            PermissionSet.CAN_REVIEW_PROOFS+',' + \
            PermissionSet.CAN_REPLY_TO_QUERIES+',' + \
            PermissionSet.CAN_CREATE_TASKS+',' + \
            PermissionSet.IS_STAFF
        executive_permission_set = PermissionSet(executive_permission_string)

        # to_binary function can place the permission in the string in any order
        # but we only care whether the permission is present or not.
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(
            sorted(map(int, executive_permission_set.to_binary())))

        # the permissions in the permission string should be true
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_ADMIN], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_STAFF], 1)

        # key with empty string should be false
        self.assertEqual(executive_permission_set.permissions[''], 0)

    def test_create_with_some_permissions_four(self):
        executive_permission_string = PermissionSet.CAN_REVIEW_PROOFS+',' + \
            PermissionSet.CAN_REPLY_TO_QUERIES+',' + \
            PermissionSet.CAN_CREATE_TASKS+',' + \
            PermissionSet.IS_STAFF

        executive_permission_set = PermissionSet(executive_permission_string)

        # to_binary function can place the permission in the string in any order
        # but we only care whether the permission is present or not.
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(
            sorted(map(int, executive_permission_set.to_binary())))

        # the permissions in the permission string should be true
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 1)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_STAFF], 1)

        # the permission not present in the string should be false
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_ADMIN], 0)

    def test_create_with_some_permissions_one(self):
        executive_permission_string = PermissionSet.CAN_REVIEW_PROOFS

        executive_permission_set = PermissionSet(executive_permission_string)

        # to_binary function can place the permission in the string in any order
        # but we only care whether the permission is present or not.
        expected_result = list(sorted(executive_permission_string.split(',')))
        actual_result = list(
            sorted(map(int, executive_permission_set.to_binary())))

        # the permissions in the permission string should be true
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REVIEW_PROOFS], 1)

        # the permission not present in the string should be false
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_CREATE_TASKS], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.CAN_REPLY_TO_QUERIES], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_STAFF], 0)
        self.assertEqual(
            executive_permission_set.permissions[PermissionSet.IS_ADMIN], 0)
