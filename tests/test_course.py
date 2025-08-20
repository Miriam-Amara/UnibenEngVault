#!/usr/bin/env python3

"""
This module contains unittest for Course class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.course import Course
from models.basemodel import BaseModel


load_dotenv()
class TestCourse(unittest.TestCase):
    """
    Implements test cases for Course class.
    """
    def setUp(self) -> None:
        self.course = Course()
        self.course.save()
        
        self.course_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.course_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")
    
    def tearDown(self) -> None:
        self.course.delete()
        self.course.save()
    
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
        self.assertIn("course_code", Course.__dict__)
        self.assertIn("semester", Course.__dict__)
        self.assertIn("credit_load", Course.__dict__)
        self.assertIn("is_optional", Course.__dict__)
        self.assertIn("title", Course.__dict__)
        self.assertIn("outline", Course.__dict__)
        self.assertIn("scope", Course.__dict__)
        self.assertIn("files", Course.__dict__)
        self.assertIn("is_active", Course.__dict__)
        self.assertIn("department", Course.__dict__)
        self.assertIn("level", Course.__dict__)
        self.assertIn("registered_by", Course.__dict__)
    
    def test_str_method(self):
        return_value = (f"[{self.course.__class__.__name__}.{self.course.id}] "
                        f"({self.course.__dict__})")
        self.assertEqual(return_value, str(self.course))

    def test_save_method(self):
        """
        Tests that instance of Course class is saved to storage.
        """
        key = f"{self.course.__class__.__name__}.{self.course.id}"
        self.assertIn(key, self.course_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Course object.
        """
        course_dict = deepcopy(self.course.__dict__)
        course_dict["created_at"] = self.course.created_at.isoformat()
        course_dict["updated_at"] = self.course.updated_at.isoformat()
        course_dict["__class__"] = self.course.__class__.__name__
        course_dict.pop("_sa_instance_state", None)
        self.assertEqual(course_dict, self.course.to_dict())
