#!/usr/bin/env python3

"""
"""


from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column

from models.basemodel import BaseModel, Base


class UserSession(BaseModel, Base):
    """
    """
    __tablename__ = "user_sessions"
    user_id = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
