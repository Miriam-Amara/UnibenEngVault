#!/usr/bin/env python3

"""
This module contains Level class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Level(BaseModel):
    name: str = ""
    registered_by: str = ""
