#!/usr/bin/env python3

"""
This module contains unittest for User class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.department import Department
from models.level import Level
from models.user import User


logger = logging.getLogger(__name__)


class TestUser(unittest.TestCase):
    """
    Implements test cases for User class.
    """

    def setUp(self) -> None:
        """
        """
        self.level = Level(name=100)
        self.department = Department(
            dept_name="electrical engineering", dept_code="eee"
        )
        storage.save()
        self.user = User(
            email="testuser@gmail.com", password="1234",
            department_id = self.department.id, level_id=self.level.id
        )
        self.user.save()

    def tearDown(self) -> None:
        """
        """
        self.level.delete()
        self.department.delete()
        self.user.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of User is an instance of User and BaseModel.
        """
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user, BaseModel)

    def test_instance_attributes(self):
        """
        Test that User class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.user.__dict__)
        self.assertIn("created_at", self.user.__dict__)
        self.assertIn("updated_at", self.user.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("email", User.__dict__)
        self.assertIn("password", User.__dict__)
        self.assertIn("role", User.__dict__)
        self.assertIn("email_verified", User.__dict__)
        self.assertIn("is_active", User.__dict__)
        self.assertIn("warnings_count", User.__dict__)
        self.assertIn("suspensions_count", User.__dict__)
        self.assertIn("department_id", User.__dict__)
        self.assertIn("level_id", User.__dict__)
        self.assertIn("department", User.__dict__)
        self.assertIn("level", User.__dict__)
        self.assertIn("warnings", User.__dict__)
        self.assertIn("suspension", User.__dict__)
        self.assertIn("admin", User.__dict__)
        self.assertIn("course_files_added", User.__dict__)
        self.assertIn("tutorial_links_added", User.__dict__)
        self.assertIn("feedbacks_added", User.__dict__)
        self.assertIn("helps_added", User.__dict__)
        self.assertIn("reports_added", User.__dict__)

    def test_str_method(self):
        """
        """
        user_dict = deepcopy(self.user.__dict__)
        user_dict.pop("_sa_instance_state")
        user_dict.pop("password")
        str_return_value = (
            f"[{self.user.__class__.__name__}.{self.user.id}] "
            f"({user_dict})"
        )
        self.assertEqual(str_return_value, str(self.user))
        logger.info(f"{str(self.user)}")

    def test_save_method(self):
        """
        Tests that instance of User class is saved to storage.
        """
        user_count = storage.count(cls="User")
        self.assertEqual(user_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of User object.
        """
        user_dict = self.user.to_dict(include_relationships=True)
        self.assertIsInstance(user_dict, dict)

        json.dumps(user_dict)
        logger.info(f"{user_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
