#!/usr/bin/env python3

"""
This module contains Faculty class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Faculty(BaseModel):
    name: str = ""
    code: str = ""
    departments: list[str] = []
    levels: list[str] = []
    registered_by: str  = ""
    admins: list[str] = []
