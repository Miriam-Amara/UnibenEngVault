#!/usr/bin/env python3

"""
This module contains Help class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Help(BaseModel):
    topic: str = ""
    message: str = ""
    is_faq: bool = False
    priority: str = ""
    status: str = ""
    response: str = ""
    sent_by: str = ""
    reviewed_by: str = ""
    