#!/usr/bin/env python3

"""

"""


from datetime import datetime
from flask import abort
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from typing import Type, TypeVar
import logging

from models import storage
from models.basemodel import BaseModel
from models.user import User, UserWarning, UserSuspension
from models.admin import Admin


logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


def get_obj(cls: Type[T], id: str) -> T | None:
    """
    """
    try:
        return storage.get_obj_by_id(cls, id)
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        abort(500)


class DatabaseOp:
    """
    """
    from models.basemodel import BaseModel
    def save(self, obj: BaseModel):
        """
        """
        try:
            obj.save()
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                detail = e.orig.diag.message_detail
                abort(409, description=detail)
            else:
                logger.error(f"Database operation failed: {e}")
                abort(500)
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)
    
    def commit(self):
        """
        """
        try:
            storage.save()
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)

    def delete(self, obj: BaseModel):
        """
        """
        try:
            obj.delete()
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)


class UserDisplineHandler:
    """
    """
    SUSPENSION_INTERVAL = 3
    MAX_WARNINGS = 9
    TERMINATION_LIMIT = 3
    db = DatabaseOp()

    def should_suspend_user(self, user: User) -> bool:
        """
        """
        warnings = user.warnings_count
        
        return (
            warnings % self.SUSPENSION_INTERVAL == 0
            and warnings <= self.MAX_WARNINGS
        )

    def should_terminate_account(self, user: User) -> bool:
        """
        """
        return user.suspensions_count >= self.TERMINATION_LIMIT

    def create_user_warning(
            self, user: User, admin: Admin,
            reason: str,
        ) -> UserWarning:
        """
        """
        warning = UserWarning(reason=reason, user_id=user.id, admin_id=admin.id)
        user.warnings_count += 1
        self.db.save(warning)
        self.db.save(user)
        return warning

    def handle_suspension(self, user: User) -> None:
        """
        """
        if self.should_suspend_user(user):
            suspension = UserSuspension(duration_days=7, user_id=user.id)
            user.suspensions_count += 1
            user.is_active = False
            self.db.save(suspension)
            self.db.save(user)
        
    def handle_termination(self, user: User) -> None:
        """
        """
        if not self.should_terminate_account(user):
            return
        self.db.delete(user)
        self.db.commit()
    
    def active_user(self, user: User) -> bool:
        """
        """
        # suspension has not expired
        if user.suspension and user.suspension.expires_at > datetime.now():
            return False
        
        # suspension has expired
        if not user.is_active:
            user.is_active = True
            self.db.save(user)
        return True
