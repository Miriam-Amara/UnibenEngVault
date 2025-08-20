#!/usr/bin/env python3

"""
This module contains TutorialLink class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class TutorialLink(BaseModel):
    course: str = ""
    url: str = ""
    title: str = ""
    content_type: str = ""
    status: str = ""
    added_by: str = ""
    approved_by: str = ""
