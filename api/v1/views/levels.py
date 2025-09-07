#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.utils import get_obj
from api.v1.data_validations import ValidateData, DatabaseOp
from models import storage
from models.level import Level


logger = logging.getLogger(__name__)


# allow only admin
@app_views.route("/admin/levels", strict_slashes=False, methods=["POST"])
def create_level():
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("LevelCreate")
    if not validated_data:
        logger.debug(f"Invalid validation class name")
        abort(500)

    level = Level(**validated_data)
    db = DatabaseOp()
    db.save(level)
    return level.to_dict(), 201

@app_views.route("/levels/<int:page_size>/<int:page_num>", strict_slashes=False, methods=["GET"])
def get_levels(page_size: int, page_num: int):
    """
    """
    level_objects = storage.all(page_size, page_num, "Level")
    if not level_objects:
        abort(404)
    all_levels = [level_obj.to_dict() for level_obj in level_objects]
    return all_levels, 200

@app_views.route("/levels/<level_id>", strict_slashes=False, methods=["GET"])
def get_level(level_id: str):
    """
    """
    level = cast(Level, get_obj("Level", level_id))
    if not level:
        abort(404)
    return level.to_dict(), 200

# allow only admins
@app_views.route("/admin/levels/<level_id>", strict_slashes=False, methods=["PUT"])
def update_level(level_id: str):
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("LevelUpdate")
    if not validated_data:
        logger.debug(f"Invalid validation class name")
        abort(500)
    level = cast(Level, get_obj("Level", level_id))
    if not level:
        abort(404)
    
    for attr, value in validated_data.items():
        setattr(level, attr, value)
    
    db = DatabaseOp()
    db.save(level)
    return level.to_dict(), 200

# allow only admins
@app_views.route("/admin/levels/<level_id>", strict_slashes=False, methods=["DELETE"])
def delete_level(level_id: str):
    level = cast(Level, get_obj("Level", level_id))
    if not level:
        abort(404)
    
    db = DatabaseOp()
    db.save(level)
    return jsonify({}), 200
