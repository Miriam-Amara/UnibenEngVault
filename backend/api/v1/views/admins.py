#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on admins.
"""


from flask import abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import get_request_data
from models import storage
from models.admin import Admin


logger = logging.getLogger(__name__)


@app_views.route(
    "/admins/<int:page_size>/<int:page_num>",
    strict_slashes=False, methods=["GET"]
)
@admin_only
def get_all_admins(page_size: int, page_num: int):
    """
    Returns all admins in the database.
    """
    admins = storage.all(Admin, page_size, page_num)
    if not admins:
        abort(404, description="Admin(s) not found")

    all_admins = [admin.to_dict() for admin in admins]
    return jsonify(all_admins), 200


@app_views.route(
        "/admins/<admin_id>", strict_slashes=False, methods=["GET"]
)
@admin_only
def get_admin_by_id(admin_id: str):
    """
    Get the details of an admin from the database.
    """
    admin = get_obj(Admin, admin_id)
    if not admin:
        abort(404, description=f"Admin does not exist")
    return jsonify(admin.to_dict()), 200


@app_views.route(
        "/admins/<admin_id>", strict_slashes=False, methods=["PUT"]
)
@admin_only
def update_admin(admin_id: str):
    """
    Updates an admin details and save to the database.
    """
    is_super_admin = get_request_data().get("is_super_admin", None)

    if not isinstance(is_super_admin, bool):
        abort(400, description="is_super_admin must be either True or False")

    admin = get_obj(Admin, admin_id)
    if not admin:
        abort(404, description="Admin does not exist")

    setattr(admin, "is_super_admin", is_super_admin)

    db = DatabaseOp()
    db.save(admin)
    return jsonify(admin.to_dict()), 200


@app_views.route(
        "/admins/<admin_id>", strict_slashes=False, methods=["DELETE"]
)
@admin_only
def delete_admin(admin_id: str):
    """
    Deletes admin from database.
    """
    admin = get_obj(Admin, admin_id)
    if not admin:
        abort(404, description=f"Admin does not exist")

    db = DatabaseOp()
    db.delete(admin)
    db.commit()
    return jsonify({}), 200
