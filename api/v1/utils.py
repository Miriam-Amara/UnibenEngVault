#!/usr/bin/env python3

"""

"""


from flask import request, abort
import logging

from models import storage
from models.basemodel import BaseModel


logger = logging.getLogger(__name__)


def get_obj(cls: str, id: str) -> BaseModel | None:
    """
    """
    try:
        return storage.get(cls, id)
    except Exception as e:
        logger.error(f"{e}")
        abort(500, description="Database operation failed.")


def get_request_data():
    """
    """
    try:
        request_json_data = request.get_json()
    except Exception:
        abort(400, description="Not a json")
    return request_json_data
