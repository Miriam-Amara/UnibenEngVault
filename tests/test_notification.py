#!/usr/bin/env python3

"""
This module contains unittest for Notification class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.notification import Notification
from models.basemodel import BaseModel


load_dotenv()


class TestNotification(unittest.TestCase):
    """
    Implements test cases for Notification class.
    """

    def setUp(self) -> None:
        self.notification = Notification()
        self.notification.save()

        self.notification_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.notification_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.notification.delete()
        self.notification.save()

    def test_instance_type(self):
        """
        Test that object of Notification is an instance
        of Notification and BaseModel.
        """
        self.assertIsInstance(self.notification, Notification)
        self.assertIsInstance(self.notification, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Notification class has instance attributes
        from BaseModel (parent) class.
        """
        self.assertIn("id", self.notification.__dict__)
        self.assertIn("created_at", self.notification.__dict__)
        self.assertIn("updated_at", self.notification.__dict__)

    def test_class_attributes(self):
        self.assertIn("title", Notification.__dict__)
        self.assertIn("message", Notification.__dict__)
        self.assertIn("source_type", Notification.__dict__)
        self.assertIn("source_id", Notification.__dict__)
        self.assertIn("sent_to", Notification.__dict__)
        self.assertIn("sent_by", Notification.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.notification.__class__.__name__}.{self.notification.id}] "
            f"({self.notification.__dict__})"
        )
        self.assertEqual(return_value, str(self.notification))

    def test_save_method(self):
        """
        Tests that instance of Notification class is saved to storage.
        """
        key = f"{self.notification.__class__.__name__}.{self.notification.id}"
        self.assertIn(key, self.notification_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Notification object.
        """
        notification_dict = deepcopy(self.notification.__dict__)
        notification_dict["created_at"] = (
            self.notification.created_at.isoformat()
        )
        notification_dict["updated_at"] = (
            self.notification.updated_at.isoformat()
        )
        notification_dict["__class__"] = self.notification.__class__.__name__
        notification_dict.pop("_sa_instance_state", None)
        self.assertEqual(notification_dict, self.notification.to_dict())
