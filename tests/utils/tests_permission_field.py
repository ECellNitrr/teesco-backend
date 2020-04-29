from django.test import TestCase
from org.custom_model_field import PermissionSet
from org.models import PermissionSetTestModel
from collections import defaultdict


class PermissionFieldTestCase(TestCase):
    # def test_reconstruction(self):
    #     vname, path, args, kwargs = my_field_instance.deconstruct()
    #     new_instance = MyField(*args, **kwargs)
    #     self.assertEqual(my_field_instance.some_attribute, new_instance.some_attribute)

    def test_create_model_obj(self):
        permission_int = 0
        permission_int |= 1 << PermissionSet.IS_STAFF
        permission_int |= 1 << PermissionSet.CAN_REVIEW_PROOFS
        
        obj = PermissionSetTestModel()
        obj.perm = PermissionSet(permission_int)
        obj.save()

        obj2 = PermissionSetTestModel.objects.get(id=obj.id)
    
        self.assertEqual(obj.id, obj2.id)
        # import pdb; pdb.set_trace()
        # self.assertFalse(obj2.perm == None)

        actual_result = obj2.perm.permissions_to_integer()
        expected_result = permission_int

        self.assertEqual(actual_result, expected_result)
