#!/usr/bin/env python3

"""
This module contains unittest for Report class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.report import Report


logger = logging.getLogger(__name__)


class TestReport(unittest.TestCase):
    """
    Implements test cases for Report class.
    """

    def setUp(self) -> None:
        """
        """
        self.report = Report(report_type="file", message="the file is corrupted")
        self.report.save()

    def tearDown(self) -> None:
        """
        """
        self.report.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of Report is an instance of Report and BaseModel.
        """
        self.assertIsInstance(self.report, Report)
        self.assertIsInstance(self.report, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Report class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.report.__dict__)
        self.assertIn("created_at", self.report.__dict__)
        self.assertIn("updated_at", self.report.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("report_type", Report.__dict__)
        self.assertIn("message", Report.__dict__)
        self.assertIn("priority", Report.__dict__)
        self.assertIn("status", Report.__dict__)
        self.assertIn("response", Report.__dict__)
        self.assertIn("file_id", Report.__dict__)
        self.assertIn("tutorial_link_id", Report.__dict__)
        self.assertIn("user_id", Report.__dict__)
        self.assertIn("admin_id", Report.__dict__)
        self.assertIn("added_by", Report.__dict__)
        self.assertIn("reviewed_by", Report.__dict__)

    def test_str_method(self):
        """
        """
        report_dict = deepcopy(self.report.__dict__)
        report_dict.pop("_sa_instance_state")
        str_return_value = (
            f"[{self.report.__class__.__name__}.{self.report.id}] "
            f"({report_dict})"
        )
        self.assertEqual(str_return_value, str(self.report))
        logger.info(f"{str(self.report)}")

    def test_save_method(self):
        """
        Tests that instance of Report class is saved to storage.
        """
        report_count = storage.count(cls="Report")
        self.assertEqual(report_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Report object.
        """
        report_dict = self.report.to_dict(include_relationships=True)
        self.assertIsInstance(report_dict, dict)
        
        json.dumps(report_dict)
        logger.info(f"{report_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
