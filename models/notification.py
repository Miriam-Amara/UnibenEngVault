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


class SentBy(enum.Enum):
    system = "system"
    admin = "admin"


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
    sent_by = mapped_column(Enum(SentBy), nullable=False)
    department_id = mapped_column(String(36), ForeignKey("departments.id"))
    level_id = mapped_column(String(36), ForeignKey("levels.id"))
    user_id = mapped_column(String(36), ForeignKey("users.id"))
    admin_id = mapped_column(String(36), ForeignKey("admins.id"))  # sent_by
