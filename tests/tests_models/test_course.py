#!/usr/bin/env python3

"""
This module contains unittest for Course class
"""

from copy import deepcopy
from typing import Any
import json
import logging
import unittest

from models import storage
from models.admin import Admin
from models.basemodel import BaseModel
from models.course import Course
from models.department import Department
from models.level import Level
from models.user import User


logger = logging.getLogger(__name__)


class TestCourse(unittest.TestCase):
    """
    Implements test cases for Course class.
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

        course_data: dict[str, Any] = {
            "course_code": "IDE551",
            "semester": "first",
            "credit_load": 3,
            "title": "Computer Programming",
            "outline": "Programming in visual basic",
            "level_id": self.level.id,
            "admin_id": self.admin.id
        }
        self.course = Course(**course_data)
        self.course.save()

    def tearDown(self) -> None:
        """
        """
        self.department.delete()
        self.level.delete()
        self.user.delete()
        self.admin.delete()
        self.course.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of Course is an instance of Course and BaseModel.
        """
        self.assertIsInstance(self.course, Course)
        self.assertIsInstance(self.course, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Course class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.course.__dict__)
        self.assertIn("created_at", self.course.__dict__)
        self.assertIn("updated_at", self.course.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("course_code", Course.__dict__)
        self.assertIn("semester", Course.__dict__)
        self.assertIn("credit_load", Course.__dict__)
        self.assertIn("title", Course.__dict__)
        self.assertIn("outline", Course.__dict__)
        self.assertIn("is_active", Course.__dict__)
        self.assertIn("level_id", Course.__dict__)
        self.assertIn("admin_id", Course.__dict__)
        self.assertIn("level", Course.__dict__)
        self.assertIn("registered_by", Course.__dict__)
        self.assertIn("files", Course.__dict__)
        self.assertIn("departments", Course.__dict__)
    
    def test_class_attribute_relationship_type(self):
        """
        """
        self.assertIsInstance(self.course.level, Level)
        self.assertIsInstance(self.course.registered_by, Admin)
        self.assertIsInstance(self.course.departments, list)
        self.assertIsInstance(self.course.files, list)

    def test_str_method(self):
        """
        """
        course_dict = deepcopy(self.course.__dict__)
        course_dict.pop("_sa_instance_state", None)
        course_dict.pop("password", None)
        str_return_value = (
            f"[{self.course.__class__.__name__}.{self.course.id}] "
            f"({course_dict})"
        )
        self.assertEqual(str_return_value, str(self.course))
        logger.info(f"{str(self.course)}")

    def test_save_method(self):
        """
        Tests that instance of Course class is saved to storage.
        """
        course_count = storage.count(cls="Course")
        self.assertEqual(course_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Course object.
        """
        self.course.save()
        course_dict = self.course.to_dict(include_relationships=True)
        self.assertIsInstance(course_dict, dict)

        json.dumps(course_dict)
        logger.info(f"{course_dict}")

if __name__=="__main__":
    unittest.main(verbosity=2)
