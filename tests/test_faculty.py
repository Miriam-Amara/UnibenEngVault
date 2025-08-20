#!/usr/bin/env python3

"""
This module contains unittest for Faculty class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.faculty import Faculty
from models.basemodel import BaseModel


load_dotenv()
class TestFaculty(unittest.TestCase):
    """
    Implements test cases for Faculty class.
    """
    def setUp(self) -> None:
        self.faculty = Faculty()
        self.faculty.save()
        
        self.faculty_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.faculty_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")
    
    def tearDown(self) -> None:
        self.faculty.delete()
        self.faculty.save()
    
    def test_instance_type(self):
        """
        Test that object of Faculty is an instance of Faculty and BaseModel.
        """
        self.assertIsInstance(self.faculty, Faculty)
        self.assertIsInstance(self.faculty, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Faculty class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.faculty.__dict__)
        self.assertIn("created_at", self.faculty.__dict__)
        self.assertIn("updated_at", self.faculty.__dict__)
    
    def test_class_attributes(self):
        self.assertIn("name", Faculty.__dict__)
        self.assertIn("code", Faculty.__dict__)
        self.assertIn("departments", Faculty.__dict__)
        self.assertIn("levels", Faculty.__dict__)
        self.assertIn("registered_by", Faculty.__dict__)
        self.assertIn("admins", Faculty.__dict__)
    
    def test_str_method(self):
        return_value = (f"[{self.faculty.__class__.__name__}.{self.faculty.id}] "
                        f"({self.faculty.__dict__})")
        self.assertEqual(return_value, str(self.faculty))

    def test_save_method(self):
        """
        Tests that instance of Faculty class is saved to storage.
        """
        key = f"{self.faculty.__class__.__name__}.{self.faculty.id}"
        self.assertIn(key, self.faculty_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Faculty object.
        """
        faculty_dict = deepcopy(self.faculty.__dict__)
        faculty_dict["created_at"] = self.faculty.created_at.isoformat()
        faculty_dict["updated_at"] = self.faculty.updated_at.isoformat()
        faculty_dict["__class__"] = self.faculty.__class__.__name__
        faculty_dict.pop("_sa_instance_state", None)
        self.assertEqual(faculty_dict, self.faculty.to_dict())
