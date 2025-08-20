#!/usr/bin/env python3

"""
This module contains Report class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Report(BaseModel):
    topic: str = ""
    message: str = ""
    priority: str = ""
    status: str = ""
    file: str = ""
    tutorial_link: str = ""
    reported_by: str = ""
    response: str = ""
    reviewed_by: str = ""
