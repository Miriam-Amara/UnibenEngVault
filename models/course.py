#!/usr/bin/env python3

"""
This module contains Course class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Course(BaseModel):
    course_code: str = ""
    semester: str = ""
    credit_load: str = ""
    is_optional: bool = False
    title: str = ""
    outline: str = ""
    scope: str = ""
    files: list[str] = []
    is_active: bool = False
    department: str = ""
    level: str = ""
    registered_by: str = ""


class CourseAssignment:
    department: str
    level: str
    course: str
