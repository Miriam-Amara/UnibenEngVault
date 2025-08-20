#!/usr/bin/env python3

"""
This module contains User class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class User(BaseModel):
    email: str = ""
    password: str = ""
    department: str = ""
    level: str = ""
    role: str = ""
    is_active: bool = True
    warnings_count: int = 0
    suspensions_count: int = 0


class UserWarning(BaseModel):
    reason: str
    user: str
    issued_by: str


class UserSuspension(BaseModel):
    reason: str
    duration_days: int
    user: str
    issued_by: str
