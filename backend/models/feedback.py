#!/usr/bin/env python3

"""Defines feedback model for the system."""


from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class FeedbackStatus(str, enum.Enum):
    pending = "pending"
    reviewed = "reviewed"


class Feedback(BaseModel, Base):
    """
    Represents feedback submitted by a user.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Feedback, e.g., message, status, etc.)
    """

    __tablename__ = "feedbacks"

    message = mapped_column(String(2000), nullable=False)
    status = mapped_column(
        Enum(FeedbackStatus, name="feedback_status", create_type=True),
        nullable=False, default="pending"
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id", ondelete="SET NULL")
    )
    added_by = relationship(
        "User", back_populates="feedbacks_added"
    )
    reviewed_by = relationship(
        "Admin", back_populates="feedbacks_reviewed"
    )
