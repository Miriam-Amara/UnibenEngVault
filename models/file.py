#!/usr/bin/env python3

"""
This module contains File class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class File(BaseModel):
    """
    Implements the File class.
    """
    name: str = ""
    course: str = ""
    file_type: str = ""
    file_format: str = ""
    session: str = ""
    size: str = ""
    status: str = ""
    rejection_reason: str = ""
    filepath: str = ""
    added_by: str = ""
    approved_by: str = ""
    