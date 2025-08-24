#!/usr/bin/env python3

"""
This module contains unittest for Help class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.help import Help
from models.basemodel import BaseModel


load_dotenv()


class TestHelp(unittest.TestCase):
    """
    Implements test cases for Help class.
    """

    def setUp(self) -> None:
        self.help = Help()
        self.help.save()

        self.help_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.help_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.help.delete()
        self.help.save()

    def test_instance_type(self):
        """
        Test that object of Help is an instance of Help and BaseModel.
        """
        self.assertIsInstance(self.help, Help)
        self.assertIsInstance(self.help, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Help class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.help.__dict__)
        self.assertIn("created_at", self.help.__dict__)
        self.assertIn("updated_at", self.help.__dict__)

    def test_class_attributes(self):
        self.assertIn("topic", Help.__dict__)
        self.assertIn("message", Help.__dict__)
        self.assertIn("is_faq", Help.__dict__)
        self.assertIn("priority", Help.__dict__)
        self.assertIn("status", Help.__dict__)
        self.assertIn("response", Help.__dict__)
        self.assertIn("sent_by", Help.__dict__)
        self.assertIn("reviewed_by", Help.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.help.__class__.__name__}.{self.help.id}] "
            f"({self.help.__dict__})"
        )
        self.assertEqual(return_value, str(self.help))

    def test_save_method(self):
        """
        Tests that instance of Help class is saved to storage.
        """
        key = f"{self.help.__class__.__name__}.{self.help.id}"
        self.assertIn(key, self.help_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Help object.
        """
        help_dict = deepcopy(self.help.__dict__)
        help_dict["created_at"] = self.help.created_at.isoformat()
        help_dict["updated_at"] = self.help.updated_at.isoformat()
        help_dict["__class__"] = self.help.__class__.__name__
        help_dict.pop("_sa_instance_state", None)
        self.assertEqual(help_dict, self.help.to_dict())
