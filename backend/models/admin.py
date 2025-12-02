#!/usr/bin/env python3

"""Defines admin-related models and permissions for the system."""


from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


class Admin(BaseModel, Base):
    """
    Represents an administrator of the system.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Admin, e.g., is_super_admin, etc.)
    """

    __tablename__ = "admins"

    is_super_admin = mapped_column(Boolean, nullable=False, default=False)
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship(
        "User",
        back_populates="admin",
        uselist=False
    )
    user_warnings_issued = relationship(
        "UserWarning",
        back_populates="issued_by"
    )
    admin_permissions = relationship(
        "AdminPermission",
        back_populates="admins",
        cascade="all, delete-orphan"
    )
    courses_added = relationship(
        "Course",
        back_populates="added_by"
    )
    files_approved = relationship(
        "File",
        back_populates="approved_by"
    )
    tutorial_links_approved = relationship(
        "TutorialLink",
        back_populates="approved_by"
    )
    feedbacks_reviewed = relationship(
        "Feedback",
        back_populates="reviewed_by"
    )
    helps_reviewed = relationship(
        "Help",
        back_populates="reviewed_by"
    )
    reports_reviewed = relationship(
        "Report",
        back_populates="reviewed_by"
    )
    from models.notification import notification_reads
    notifications = relationship(
        "Notification",
        secondary="notification_reads",
        back_populates="admin",
    )


class Permission(BaseModel, Base):
    """
    Represents a type of permission that can be granted to admins.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Permission, e.g., use_case, etc.)
    """

    __tablename__ = "permissions"

    use_case = mapped_column(String(200), nullable=False)
    admin_permissions = relationship(
        "AdminPermission",
        back_populates="permissions",
        viewonly=True,
        cascade="all, delete-orphan",
    )


class AdminPermission(BaseModel, Base):
    """
    Represents the mapping between an admin and their permissions.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to AdminPermission, e.g., admin_id, etc.)
    """

    __tablename__ = "admin_permissions"

    admin_id = mapped_column(
        String(36), ForeignKey("admins.id"), unique=True, nullable=False
    )
    department_id = mapped_column(
        String(36), ForeignKey("departments.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    )
    level_id = mapped_column(
        String(36), ForeignKey("levels.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    )
    permission_id = mapped_column(
        String(36), ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    )

    admins = relationship(
        "Admin",
        back_populates="admin_permissions"
    )
    departments = relationship(
        "Department",
        back_populates="admin_permissions"
    )
    levels = relationship(
        "Level",
        back_populates="admin_permissions"
    )
    permissions = relationship(
        "Permission",
        back_populates="admin_permissions"
    )
