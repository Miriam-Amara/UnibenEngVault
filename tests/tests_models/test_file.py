#!/usr/bin/env python3

"""
This module contains unittest for File class
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
from models.file import File
from models.department import Department
from models.level import Level
from models.user import User


logger = logging.getLogger(__name__)


class TestFile(unittest.TestCase):
    """
    Implements test cases for File class.
    """

    def setUp(self) -> None:
        """
        """
        self.department = Department(dept_name="electrical engineering", dept_code="eee")
        self.level = Level(name=100)
        self.user1 = User(
            email="heroko@gmail.com", password="ghyiii",
            department_id = self.department.id, level_id=self.level.id
        )
        self.user2 = User(
            email="testuser@gmail.com", password="1234", role="admin",
            department_id = self.department.id, level_id=self.level.id
        )
        storage.save()

        self.admin = Admin(is_super_admin=True, user_id=self.user2.id)
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

        file_data: dict[str, Any] = {
            "file_name": "IDE551_past_question_2020-2021_456789.pdf",
            "file_type": "past_question",
            "file_format": "pdf",
            "session": "2020-2021",
            "size": 34,
            "filepath": "500/first/industrial-engineering/ide551/file_name",
            "course_id": self.course.id,
            "user_id": self.user1.id,
            "admin_id": self.admin.id,
        }
        self.file = File(**file_data)
        self.file.save()

    def tearDown(self) -> None:
        """
        """
        self.department.delete()
        self.level.delete()
        self.user1.delete()
        self.user2.delete()
        self.admin.delete()
        self.course.delete()
        self.file.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of File is an instance of File and BaseModel.
        """
        self.assertIsInstance(self.file, File)
        self.assertIsInstance(self.file, BaseModel)

    def test_instance_attributes(self):
        """
        Test that File class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.file.__dict__)
        self.assertIn("created_at", self.file.__dict__)
        self.assertIn("updated_at", self.file.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("file_name", File.__dict__)
        self.assertIn("file_type", File.__dict__)
        self.assertIn("file_format", File.__dict__)
        self.assertIn("session", File.__dict__)
        self.assertIn("size", File.__dict__)
        self.assertIn("status", File.__dict__)
        self.assertIn("rejection_reason", File.__dict__)
        self.assertIn("filepath", File.__dict__)
        self.assertIn("course_id", File.__dict__)
        self.assertIn("user_id", File.__dict__)
        self.assertIn("admin_id", File.__dict__)
        self.assertIn("course", File.__dict__)
        self.assertIn("added_by", File.__dict__)
        self.assertIn("approved_by", File.__dict__)

    def test_str_method(self):
        """
        """
        file_dict = deepcopy(self.file.__dict__)
        file_dict.pop("_sa_instance_state", None)
        str_return_value = (
            f"[{self.file.__class__.__name__}.{self.file.id}] "
            f"({file_dict})"
        )
        self.assertEqual(str_return_value, str(self.file))
        logger.info(f"{str(self.file)}")

    def test_save_method(self):
        """
        Tests that instance of File class is saved to storage.
        """
        file_count = storage.count(cls="File")
        self.assertEqual(file_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of File object.
        """
        file_dict = self.file.to_dict(include_relationships=True)
        self.assertIsInstance(file_dict, dict)

        json.dumps(file_dict)
        logger.info(f"{file_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
