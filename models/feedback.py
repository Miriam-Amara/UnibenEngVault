#!/usr/bin/env python3

"""
This module contains Feedback class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Feedback(BaseModel):
    message: str = ""
    status: str = ""
    added_by: str = ""
    reviewed_by: str = ""
    