#!/usr/bin/env python3

"""
This module contains unittest for TutorialLink class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.tutoriallink import TutorialLink
from models.basemodel import BaseModel


load_dotenv()
class TestTutorialLink(unittest.TestCase):
    """
    Implements test cases for TutorialLink class.
    """
    def setUp(self) -> None:
        self.tutoriallink = TutorialLink()
        self.tutoriallink.save()
        
        self.tutoriallink_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.tutoriallink_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")
    
    def tearDown(self) -> None:
        self.tutoriallink.delete()
        self.tutoriallink.save()
    
    def test_instance_type(self):
        """
        Test that object of TutorialLink is an instance of TutorialLink and BaseModel.
        """
        self.assertIsInstance(self.tutoriallink, TutorialLink)
        self.assertIsInstance(self.tutoriallink, BaseModel)

    def test_instance_attributes(self):
        """
        Test that TutorialLink class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.tutoriallink.__dict__)
        self.assertIn("created_at", self.tutoriallink.__dict__)
        self.assertIn("updated_at", self.tutoriallink.__dict__)
    
    def test_class_attributes(self):
        self.assertIn("course", TutorialLink.__dict__)
        self.assertIn("url", TutorialLink.__dict__)
        self.assertIn("title", TutorialLink.__dict__)
        self.assertIn("content_type", TutorialLink.__dict__)
        self.assertIn("status", TutorialLink.__dict__)
        self.assertIn("added_by", TutorialLink.__dict__)
        self.assertIn("approved_by", TutorialLink.__dict__)

    def test_str_method(self):
        return_value = (f"[{self.tutoriallink.__class__.__name__}.{self.tutoriallink.id}] "
                        f"({self.tutoriallink.__dict__})")
        self.assertEqual(return_value, str(self.tutoriallink))

    def test_save_method(self):
        """
        Tests that instance of TutorialLink class is saved to storage.
        """
        key = f"{self.tutoriallink.__class__.__name__}.{self.tutoriallink.id}"
        self.assertIn(key, self.tutoriallink_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of TutorialLink object.
        """
        tutoriallink_dict = deepcopy(self.tutoriallink.__dict__)
        tutoriallink_dict["created_at"] = self.tutoriallink.created_at.isoformat()
        tutoriallink_dict["updated_at"] = self.tutoriallink.updated_at.isoformat()
        tutoriallink_dict["__class__"] = self.tutoriallink.__class__.__name__
        tutoriallink_dict.pop("_sa_instance_state", None)
        self.assertEqual(tutoriallink_dict, self.tutoriallink.to_dict())
