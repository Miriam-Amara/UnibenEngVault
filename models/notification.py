#!/usr/bin/env python3

"""Defines the Notification model for the system."""


from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import mapped_column
import enum

from models.basemodel import BaseModel, Base


class NotificationType(enum.Enum):
    general = "general"
    faculty = "faculty"
    departmental = "departmental"
    departmental_level = "departmental_level"
    user = "user"


class Notification(BaseModel, Base):
    """
    Represents a notification sent to a user.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Notification, e.g., message, type, etc.)
    """

    __tablename__ = "notifications"

    notification_type = mapped_column(Enum(NotificationType), nullable=False)
    message = mapped_column(String(2000), nullable=False)
    department_id = mapped_column(
        String(36), ForeignKey("departments.id", ondelete="SET NULL")
    )
    level_id = mapped_column(
        String(36), ForeignKey("levels.id", ondelete="SET NULL")
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id", ondelete="SET NULL")
    )
