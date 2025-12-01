#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify, request
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


def get_level_dict(level: Level) -> dict[str, int]:
    """
    Returns a json serializable dict of the level object.
    """
    level_dict = level.to_dict()
    level_dict["no_of_users_in_level"] = len(level.users)
    level_dict["no_of_courses_in_level"] = len(level.courses) 
    level_dict.pop("__class__", None)

    return level_dict


@app_views.route("/levels", strict_slashes=False, methods=["POST"])
@admin_only
def create_level():
    """
    Create and add new level to the database.
    """
    valid_data = validate_request_data(LevelCreate)

    level = Level(**valid_data)
    db = DatabaseOp()
    db.save(level)

    level_dict = get_level_dict(level)
    return jsonify(level_dict), 201


@app_views.route(
        "/levels",
        strict_slashes=False,
        methods=["GET"]
    )
def get_all_levels():
    """
    Returns all levels with optional date filtering, search and pagination.
    """
    page_size: str | None = request.args.get("page_size")
    page_num: str | None = request.args.get("page_num")
    created_at: str | None = request.args.get("created_at")
    search_str: str | None = request.args.get("search_str")

    if search_str:
        levels = storage.search(
            Level, search_str, page_size=page_size, page_num=page_num
        )
    else:
        levels = storage.all(
            Level, page_size=page_size, page_num=page_num, date_time=created_at
        )

    if not levels:
        abort(404, description="No level found.")

    all_levels = [get_level_dict(level) for level in levels]
    return jsonify(all_levels), 200


@app_views.route(
        "/levels/<level_id>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_level(level_id: str):
    """
    Return a level by its id.
    """
    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")

    return jsonify(get_level_dict(level)), 200


@app_views.route(
        "/levels/<level_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
@admin_only
def delete_level(level_id: str):
    """
    Delete a level given the level id.
    """
    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")
    
    db = DatabaseOp()
    db.delete(level)
    db.commit()
    return jsonify({}), 200
