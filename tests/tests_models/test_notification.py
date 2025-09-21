#!/usr/bin/env python3

"""
This module contains unittest for Notification class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.notification import Notification


logger = logging.getLogger(__name__)


class TestNotification(unittest.TestCase):
    """
    Implements test cases for Notification class.
    """

    def setUp(self) -> None:
        """
        """
        self.notification = Notification(
            notification_type="departmental",
            message="All courses have been added. Please check"
        )
        self.notification.save()

    def tearDown(self) -> None:
        """
        """
        self.notification.delete()
        storage.save()

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
        """
        """
        self.assertIn("notification_type", Notification.__dict__)
        self.assertIn("message", Notification.__dict__)
        self.assertIn("department_id", Notification.__dict__)
        self.assertIn("level_id", Notification.__dict__)
        self.assertIn("user_id", Notification.__dict__)
        self.assertIn("admin_id", Notification.__dict__)

    def test_str_method(self):
        """
        """
        notification_dict = deepcopy(self.notification.__dict__)
        notification_dict.pop("_sa_instance_state")
        str_return_value = (
            f"[{self.notification.__class__.__name__}.{self.notification.id}] "
            f"({notification_dict})"
        )
        self.assertEqual(str_return_value, str(self.notification))
        logger.info(f"{str(self.notification)}")

    def test_save_method(self):
        """
        Tests that instance of Notification class is saved to storage.
        """
        notification_count = storage.count(cls="Notification")
        self.assertEqual(notification_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Notification object.
        """
        notification_dict = self.notification.to_dict()
        self.assertIsInstance(notification_dict, dict)

        json.dumps(notification_dict)
        logger.info(f"{notification_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
