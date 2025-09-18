#!/usr/bin/env python3

"""

"""


from flask import g, abort, jsonify
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils import get_obj, get_request_data
from api.v1.data_validations import DatabaseOp
from models import storage
from models.admin import Admin
from models.user import User




logger = logging.getLogger(__name__)



@app_views.route("/admins", strict_slashes=False, methods=["POST"])
@admin_only
def create_admin():
    """
    """
    admin_data = get_request_data()
    user_id = admin_data.get("user_id", None)
    is_super_admin = admin_data.get("is_super_admin", None)
    if not user_id or not isinstance(user_id, str):
        abort(400, description="Missing user_id")
    if not is_super_admin or not isinstance(is_super_admin, bool):
        abort(400, description="is_super_admin must be either true or false")
    
    admin = Admin(**admin_data)
    db = DatabaseOp()
    db.save(admin)
    return jsonify(admin.to_dict()), 201

@app_views.route("/admins/<int:page_size>/<int:page_num>", strict_slashes=False, methods=["GET"])
@admin_only
def get_admins(page_size: int, page_num: int):
    """
    """
    admins_objects = storage.all(page_size, page_num, "Admin")
    if not admins_objects:
        abort(404, description="no admin found")
    
    all_admins = [admin.to_dict() for admin in admins_objects]
    return jsonify(all_admins), 200

@app_views.route("/admins/<admin_id>", strict_slashes=False, methods=["GET"])
@admin_only
def get_admin(admin_id: str):
    """
    """
    admin = getattr(g, "current_user", None)
    if admin_id == "me" and not admin:
        abort(404, description=f"admin with id: {admin_id} does not exist.")
    else:   
        admin = cast(Admin, get_obj("Admin", admin_id))
        if not admin:
            abort(404, description=f"admin with id: {admin_id} does not exist.")
    return jsonify(admin.to_dict()), 200

@app_views.route("/admins/<admin_id>", strict_slashes=False, methods=["PUT"])
@admin_only
def update_admin(admin_id: str):
    """
    """
    admin_data = get_request_data()
    if not admin_data:
        abort(400)

    user_id = admin_data.get("user_id", None)
    is_super_admin = admin_data.get("is_super_admin", None)
    if user_id:
        user = cast(User, get_obj("User", user_id))
        if not user:
            abort(404, description=f"user with id: {user_id} does not exist.")
    if is_super_admin and not isinstance(is_super_admin, bool):
        abort(400, description="is_super_admin must be either true or false.")
    
    admin = getattr(g, "current_user", None)
    if admin_id == "me" and not admin:
        abort(404, description=f"admin with id: {admin_id} does not exist.")
    else:   
        admin = cast(Admin, get_obj("Admin", admin_id))
        if not admin:
            abort(404, description=f"admin with id: {admin_id} does not exist.")
    for attr, value in admin_data.items():
        setattr(admin, attr, value)
    
    db = DatabaseOp()
    db.save(admin)

    return jsonify(admin.to_dict()), 200

@app_views.route("/admins/<admin_id>", strict_slashes=False, methods=["DELETE"])
@admin_only
def delete_admin(admin_id: str):
    """
    """
    admin = getattr(g, "current_user", None)
    if admin_id == "me" and not admin:
        abort(404, description=f"admin with id: {admin_id} does not exist.")
    else:   
        admin = cast(Admin, get_obj("Admin", admin_id))
        if not admin:
            abort(404, description=f"admin with id: {admin_id} does not exist.")
    db = DatabaseOp()
    db.delete(admin)
    db.commit()
    return jsonify({}), 200
