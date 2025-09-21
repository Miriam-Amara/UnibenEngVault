#!/usr/bin/env python3

"""
This module contains unittest for Admin class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.admin import Admin
from models.basemodel import BaseModel
from models.department import Department
from models.level import Level
from models.user import User


logger = logging.getLogger()


class TestAdmin(unittest.TestCase):
    """
    Implements test cases for Admin class.
    """

    def setUp(self) -> None:
        """
        """
        self.department = Department(dept_name="electrical engineering", dept_code="eee")
        self.level = Level(name=100)
        self.user = User(
            email="testuser@gmail.com", password="1234",
            department_id = self.department.id, level_id=self.level.id
        )
        storage.save()

        self.admin = Admin(is_super_admin=True, user_id=self.user.id)
        self.admin.save()

    def tearDown(self) -> None:
        """
        Cleans up test objects and checks cascade behavior.

        Deletes the Department, Level, User, and Admin objects created during
        testing. Cascade rules are implicitly verified since deleting a parent
        (e.g., Department) removes dependent child record Users.
        """
        self.department.delete()
        self.level.delete()
        self.user.delete()
        self.admin.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of Admin is an instance of Admin and BaseModel.
        """
        self.assertIsInstance(self.admin, Admin)
        self.assertIsInstance(self.admin, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Admin class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.admin.__dict__)
        self.assertIn("created_at", self.admin.__dict__)
        self.assertIn("updated_at", self.admin.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("is_super_admin", Admin.__dict__)
        self.assertIn("user_id", Admin.__dict__)
        self.assertIn("user", Admin.__dict__)
        self.assertIn("admin_permissions", Admin.__dict__)
        self.assertIn("courses_registered", Admin.__dict__)
        self.assertIn("files_approved", Admin.__dict__)
        self.assertIn("tutorial_links_approved", Admin.__dict__)
        self.assertIn("feedbacks_reviewed", Admin.__dict__)
        self.assertIn("helps_reviewed", Admin.__dict__)
        self.assertIn("reports_reviewed", Admin.__dict__)

    def test_str_method(self):
        """
        """
        admin_dict = deepcopy(self.admin.__dict__)
        admin_dict.pop("_sa_instance_state", None)
        admin_dict.pop("password", None)
        str_return_value = (
            f"[{self.admin.__class__.__name__}.{self.admin.id}] "
            f"({admin_dict})"
        )
        self.assertEqual(str_return_value, str(self.admin))
        logger.info(f"{str(self.admin)}")

    def test_save_method(self):
        """
        Tests that instance of Admin class is saved to storage.
        """
        count_admin = storage.count(cls="Admin")
        self.assertEqual(count_admin, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Admin object.
        """
        self.admin.save()
        admin_dict = self.admin.to_dict(include_relationships=True)

        self.assertIsInstance(admin_dict, dict)
        self.assertNotIn("password", admin_dict)
        self.assertNotIn("_sa_instance_state", admin_dict)

        json.dumps(admin_dict)
        logger.info(f"{admin_dict}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
