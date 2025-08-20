#!/usr/bin/env python3

"""
This module contains Admin class for UnibenEngVault.
"""

from models.basemodel import BaseModel


class Admin(BaseModel):
    is_super_admin: bool = False
    user: str = ""
    admin_permissions: list[str] = []


class Permission(BaseModel):
    use_case:str

class AdminPermission:
    admin: str = ""
    permissions: list[str] = []
    department: str = ""
    level: str = ""
