#!/usr/bin/env python3

"""
This module contains unittest for File class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.file import File
from models.basemodel import BaseModel


load_dotenv()
class TestFile(unittest.TestCase):
    """
    Implements test cases for File class.
    """
    def setUp(self) -> None:
        self.file = File()
        self.file.save()
        
        self.file_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.file_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")
    
    def tearDown(self) -> None:
        self.file.delete()
        self.file.save()
    
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
        self.assertIn("name", File.__dict__)
        self.assertIn("course", File.__dict__)
        self.assertIn("file_type", File.__dict__)
        self.assertIn("file_format", File.__dict__)
        self.assertIn("session", File.__dict__)
        self.assertIn("size", File.__dict__)
        self.assertIn("status", File.__dict__)
        self.assertIn("rejection_reason", File.__dict__)
        self.assertIn("filepath", File.__dict__)
        self.assertIn("added_by", File.__dict__)
        self.assertIn("approved_by", File.__dict__)
    
    def test_str_method(self):
        return_value = (f"[{self.file.__class__.__name__}.{self.file.id}] "
                        f"({self.file.__dict__})")
        self.assertEqual(return_value, str(self.file))

    def test_save_method(self):
        """
        Tests that instance of File class is saved to storage.
        """
        key = f"{self.file.__class__.__name__}.{self.file.id}"
        self.assertIn(key, self.file_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of File object.
        """
        file_dict = deepcopy(self.file.__dict__)
        file_dict["created_at"] = self.file.created_at.isoformat()
        file_dict["updated_at"] = self.file.updated_at.isoformat()
        file_dict["__class__"] = self.file.__class__.__name__
        file_dict.pop("_sa_instance_state", None)
        self.assertEqual(file_dict, self.file.to_dict())
