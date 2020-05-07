from django.test import TestCase
from org.custom_model_field import PermissionSet
from org.models import PermissionSetTestModel
from collections import defaultdict


class PermissionFieldTestCase(TestCase):
    "These testcases are for org.custom_model_field.PermissionField class"


    def test_create_model_obj(self):
        # create a permissionset record (say managers) for testing 
        permission_int = 0
        permission_int |= 1 << PermissionSet.IS_STAFF
        permission_int |= 1 << PermissionSet.CAN_REVIEW_PROOFS
        permission_int |= 1 << PermissionSet.CAN_REPLY_TO_QUERIES
        
        original_record = PermissionSetTestModel()
        original_record.perm = PermissionSet(permission_int)
        original_record.save()

        record_from_db = PermissionSetTestModel.objects.get(id=original_record.id)
    
        # check querying
        self.assertEqual(original_record.id, record_from_db.id)
        
        # check permissions are equal between records
        actual_result = record_from_db.perm.permissions_to_integer()
        expected_result = permission_int

        self.assertEqual(actual_result, expected_result)

        # check permissions with help of permissions dictionary
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.CAN_CREATE_TASKS])

        self.assertTrue(record_from_db.perm.permissions[PermissionSet.IS_STAFF])
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.CAN_REVIEW_PROOFS])
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])


    
    def test_updating_with_new_perm_obj(self):
        # create a permission set record
        permission_int = 0
        permission_int |= 1 << PermissionSet.IS_STAFF
        
        original_record = PermissionSetTestModel()
        original_record.perm = PermissionSet(permission_int)
        original_record.save()

        # fetch from db
        record_from_db = PermissionSetTestModel.objects.get(id=original_record.id)
        
        # change the  permissions
        new_perm_int = 0
        new_perm_int |= 1 << PermissionSet.IS_ADMIN
        new_perm_int |= 1 << PermissionSet.CAN_REPLY_TO_QUERIES
        new_perm_int |= 1 << PermissionSet.CAN_CREATE_TASKS

        record_from_db.perm = PermissionSet(new_perm_int)
        record_from_db.save()

        # fetch again from db
        updated_record = PermissionSetTestModel.objects.get(id=original_record.id)

        # check permissions int 
        self.assertEqual(updated_record.perm.permissions_to_integer(), new_perm_int)

        # check permissions with help of permissions dictionary
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.IS_ADMIN])
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.CAN_CREATE_TASKS])

        self.assertFalse(record_from_db.perm.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.CAN_REVIEW_PROOFS])


    def test_updating_with_setter_func(self):
        # create a permission set record
        permission_int = 0
        permission_int |= 1 << PermissionSet.IS_STAFF
        
        original_record = PermissionSetTestModel()
        original_record.perm = PermissionSet(permission_int)
        original_record.save()

        # fetch from db
        record_from_db = PermissionSetTestModel.objects.get(id=original_record.id)
        
        # change the  permissions
        new_perm_list = [
            PermissionSet.IS_ADMIN,
            PermissionSet.CAN_REPLY_TO_QUERIES,
            PermissionSet.CAN_CREATE_TASKS
        ]
        record_from_db.perm.set_permissions(new_perm_list)
        record_from_db.save()

        # fetch again from db
        updated_record = PermissionSetTestModel.objects.get(id=original_record.id)

        # check permissions with help of permissions dictionary
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.IS_ADMIN])
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertTrue(record_from_db.perm.permissions[PermissionSet.CAN_CREATE_TASKS])

        self.assertFalse(record_from_db.perm.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.CAN_REVIEW_PROOFS])


    def test_multiple_record_creation(self):
        # create a permission set records
        p_one = 1 << PermissionSet.IS_ADMIN
        p_two = 1 << PermissionSet.IS_STAFF
        p_three = 1 << PermissionSet.CAN_CREATE_TASKS
        p_four = 1 << PermissionSet.CAN_REPLY_TO_QUERIES
        p_five = 1 << PermissionSet.CAN_REVIEW_PROOFS

        PermissionSetTestModel.objects.create(perm=PermissionSet(p_one))
        PermissionSetTestModel.objects.create(perm=PermissionSet(p_two))
        PermissionSetTestModel.objects.create(perm=PermissionSet(p_three))
        PermissionSetTestModel.objects.create(perm=PermissionSet(p_four))
        PermissionSetTestModel.objects.create(perm=PermissionSet(p_five))

        # fetch from db
        records = PermissionSetTestModel.objects.all().order_by('-id')[:5]
        records = list(reversed(records))
        
        # verify the permissions
        self.assertEqual(records[0].perm.permissions_to_integer(), p_one)
        self.assertEqual(records[1].perm.permissions_to_integer(), p_two)
        self.assertEqual(records[2].perm.permissions_to_integer(), p_three)
        self.assertEqual(records[3].perm.permissions_to_integer(), p_four)
        self.assertEqual(records[4].perm.permissions_to_integer(), p_five)


    def test_create_with_no_perm_obj(self):
        # create permission record without providing perm obj
        # default behaviour is to return an empty permissions obj
        PermissionSetTestModel.objects.create()

        # fetch from db
        record_from_db = PermissionSetTestModel.objects.last()

        # check permissions with help of permissions dictionary
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.IS_ADMIN])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.CAN_REPLY_TO_QUERIES])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.CAN_CREATE_TASKS])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.IS_STAFF])
        self.assertFalse(record_from_db.perm.permissions[PermissionSet.CAN_REVIEW_PROOFS])