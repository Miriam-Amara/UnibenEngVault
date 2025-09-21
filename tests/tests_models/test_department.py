#!/usr/bin/env python3

"""
This module contains unittest for Department class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.department import Department


logger = logging.getLogger(__name__)


class TestDepartment(unittest.TestCase):
    """
    Implements test cases for Department class.
    """

    def setUp(self) -> None:
        """
        """
        self.department = Department(dept_name="computer engineering", dept_code="cpe")
        self.department.save()

    def tearDown(self) -> None:
        """
        """
        self.department.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of Department is an instance of
        Department and BaseModel.
        """
        self.assertIsInstance(self.department, Department)
        self.assertIsInstance(self.department, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Department class has instance attributes
        from BaseModel (parent) class.
        """
        self.assertIn("id", self.department.__dict__)
        self.assertIn("created_at", self.department.__dict__)
        self.assertIn("updated_at", self.department.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("dept_name", Department.__dict__)
        self.assertIn("dept_code", Department.__dict__)
        self.assertIn("users", Department.__dict__)
        self.assertIn("courses", Department.__dict__)
        self.assertIn("admin_permissions", Department.__dict__)

    def test_str_method(self):
        """
        """
        dept_dict = deepcopy(self.department.__dict__)
        dept_dict.pop("_sa_instance_state", None)
        str_return_value = (
            f"[{self.department.__class__.__name__}.{self.department.id}] "
            f"({dept_dict})"
        )
        self.assertEqual(str_return_value, str(self.department))
        logger.info(f"{str(self.department)}")

    def test_save_method(self):
        """
        Tests that instance of Department class is saved to storage.
        """
        dept_count = storage.count(cls="Department")
        self.assertEqual(dept_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Department object.
        """
        dept_dict = self.department.to_dict(include_relationships=True)
        self.assertIsInstance(dept_dict, dict)

        json.dumps(dept_dict)
        logger.info(f"{dept_dict}")

if __name__=="__main__":
    unittest.main(verbosity=2)
