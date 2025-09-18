#!/usr/bin/env python3

"""

"""
from flask import g, abort
from typing import Callable, Any, TypeVar, cast
import functools
import logging


logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


def admin_only(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        """
        logger.debug("In authorization")
        user = getattr(g, "current_user", None)
        if not user:
            abort(401)
        user = g.current_user
        logger.debug(f"{user}")
        logger.debug(f"{user.role.value}")
        if user.role.value != "admin":
            abort(403)
        return func(*args, **kwargs)
    return cast(F, wrapper)
