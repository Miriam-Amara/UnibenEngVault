#!/usr/bin/env python3

"""
This module contains unittest for Level class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.level import Level
from models.basemodel import BaseModel


load_dotenv()
class TestLevel(unittest.TestCase):
    """
    Implements test cases for Level class.
    """
    def setUp(self) -> None:
        self.level = Level()
        self.level.save()
        
        self.level_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.level_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")
    
    def tearDown(self) -> None:
        self.level.delete()
        self.level.save()
    
    def test_instance_type(self):
        """
        Test that object of Level is an instance of Level and BaseModel.
        """
        self.assertIsInstance(self.level, Level)
        self.assertIsInstance(self.level, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Level class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.level.__dict__)
        self.assertIn("created_at", self.level.__dict__)
        self.assertIn("updated_at", self.level.__dict__)
    
    def test_class_attributes(self):
        self.assertIn("name", Level.__dict__)
        self.assertIn("registered_by", Level.__dict__)
        
    def test_str_method(self):
        return_value = (f"[{self.level.__class__.__name__}.{self.level.id}] "
                        f"({self.level.__dict__})")
        self.assertEqual(return_value, str(self.level))

    def test_save_method(self):
        """
        Tests that instance of Level class is saved to storage.
        """
        key = f"{self.level.__class__.__name__}.{self.level.id}"
        self.assertIn(key, self.level_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Level object.
        """
        level_dict = deepcopy(self.level.__dict__)
        level_dict["created_at"] = self.level.created_at.isoformat()
        level_dict["updated_at"] = self.level.updated_at.isoformat()
        level_dict["__class__"] = self.level.__class__.__name__
        level_dict.pop("_sa_instance_state", None)
        self.assertEqual(level_dict, self.level.to_dict())
