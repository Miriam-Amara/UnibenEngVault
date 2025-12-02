#!/usr/bin/env python3

"""
Defines UserSession class for tracking user's sessions
in the database.
"""


from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


class UserSession(BaseModel, Base):
    """
    Keeps track user sessions in the databasee.
    """
    __tablename__ = "user_sessions"
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship(
        "User",
        back_populates="user_session",
    )
