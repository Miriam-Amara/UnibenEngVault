#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    validate_request_data, LevelCreate
)
from models import storage
from models.level import Level


logger = logging.getLogger(__name__)


@app_views.route("/levels", strict_slashes=False, methods=["POST"])
@admin_only
def create_level():
    """
    """
    valid_data = validate_request_data(LevelCreate)

    level = Level(**valid_data)
    db = DatabaseOp()
    db.save(level)

    return jsonify(level.to_dict()), 201


@app_views.route(
        "/levels/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_all_levels(page_size: int, page_num: int):
    """
    """
    levels = storage.all(Level, page_size, page_num)
    if not levels:
        abort(404, description="no level found")

    all_levels = [level.to_dict() for level in levels]
    return jsonify(all_levels), 200


@app_views.route(
        "/levels/<level_id>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_level(level_id: str):
    """
    """
    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")

    return jsonify(level.to_dict()), 200


@app_views.route(
        "/levels/<level_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
@admin_only
def delete_level(level_id: str):
    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")
    
    db = DatabaseOp()
    db.delete(level)
    db.commit()
    return jsonify({}), 200
