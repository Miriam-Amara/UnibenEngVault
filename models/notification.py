#!/usr/bin/env python3

"""
This module contains Notification class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Notification(BaseModel):
    title: str = ""
    message: str = ""
    source_type: str = ""
    source_id: str = ""
    sent_to: str = ""
    sent_by: str = ""
