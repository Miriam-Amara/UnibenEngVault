#!/usr/bin/env python3

"""Defines the Help model for the system."""


from sqlalchemy import String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class HelpType(enum.Enum):
    technical = "technical"
    academic = "academic"
    account = "account"
    other = "other"


class HelpStatus(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    resolved = "resolved"


class HelpPriority(enum.Enum):
    low = "low"
    high = "high"


class Help(BaseModel, Base):
    """
    Represents a help request submitted by a user.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Help, e.g., type, message, status, etc.)
    """

    __tablename__ = "helps"

    help_type = mapped_column(Enum(HelpType), nullable=False)
    message = mapped_column(String(2000), nullable=False)
    is_faq = mapped_column(Boolean, nullable=False, default=False)
    priority = mapped_column(Enum(HelpPriority), nullable=False, default="low")
    status = mapped_column(Enum(HelpStatus), nullable=False, default="pending")
    response = mapped_column(String(2000))
    user_id = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id"), nullable=False
    )

    added_by = relationship(
        "User", back_populates="helps_added", viewonly=True
    )
    reviewed_by = relationship(
        "Admin", back_populates="helps_reviewed", viewonly=True
    )
