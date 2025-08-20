#!/usr/bin/env python3

"""
This module contains Department class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Department(BaseModel):
    name: str = ""
    code: str = ""
    faculty: str = ""
    course_assignments: list[str] = []
    registered_by: str = ""
