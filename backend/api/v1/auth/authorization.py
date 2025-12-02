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
        """ """
        user = getattr(g, "current_user", None)
        if not user:
            abort(403)
        user = g.current_user
        if not user.is_admin:
            abort(403)
        return func(*args, **kwargs)

    return cast(F, wrapper)
