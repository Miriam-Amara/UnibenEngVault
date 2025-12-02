#!/usr/bin/env python3

"""
"""

from flask import g, abort, jsonify
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    validate_request_data,
    ReportCreate,
    ReportUpdate,
)
from api.v1.auth.authorization import admin_only
from models import storage
from models.admin import Admin
from models.file import File
from models.notification import Notification
from models.report import Report
from models.tutoriallink import TutorialLink
from models.user import User


logger = logging.getLogger(__name__)


def add_notification(message: str, report_id: str) -> None:
    """ """
    data = {
        "notification_scope": "admin",
        "message": message,
        "report_id": report_id,
    }
    notification = Notification(**data)
    db = DatabaseOp()
    db.save(notification)


@app_views.route("/reports", strict_slashes=False, methods=["POST"])
def add_report():
    """ """
    user = cast(User, g.current_user)

    valid_data = validate_request_data(ReportCreate)

    if "file_d" in valid_data:
        file = get_obj(File, valid_data["file_id"])
        if not file:
            abort(404, description="File does not exist.")

    if "tutorial_link_id" in valid_data:
        tutorial_link = get_obj(TutorialLink, valid_data["tutorial_link_id"])
        if not tutorial_link:
            abort(404, description="Tutorial link does not exist.")

    db = DatabaseOp()
    valid_data["added_by"] = user
    report = Report(**valid_data)
    db.save(report)

    add_notification(valid_data["message"], report.id)
    return jsonify(report.to_dict()), 201


@app_views.route(
    "/reports/<int:page_size>/<int:page_num>",
    strict_slashes=False,
    methods=["GET"]
)
@admin_only
def get_all_reports(page_size: int, page_num: int):
    """ """
    reports = storage.all(Report, page_size, page_num)
    if not reports:
        abort(404, description="No reports found.")

    all_reports = [report.to_dict() for report in reports]
    return jsonify(all_reports), 200


@app_views.route(
        "/reports/<report_id>", strict_slashes=False, methods=["GET"]
)
@admin_only
def get_reports_by_user(report_id: str):
    """ """
    report = get_obj(Report, report_id)
    if not report:
        abort(404, description="Report does not exist.")

    report_dict = report.to_dict()
    return jsonify(report_dict), 200


@app_views.route(
        "/reports/<report_id>", strict_slashes=False, methods=["PUT"]
)
@admin_only
def update_report(report_id: str):
    """ """
    admin: Admin = cast(Admin, g.current_user.admin)

    valid_data = validate_request_data(ReportUpdate)
    valid_data["reviewed_by"] = admin

    report = get_obj(Report, report_id)
    if not report:
        abort(404, description="Report does not exist.")

    for attr, value in valid_data.items():
        setattr(report, attr, value)

    db = DatabaseOp()
    db.save(report)
    return jsonify(report.to_dict()), 200


@app_views.route(
        "/reports/<report_id>", strict_slashes=False, methods=["DELETE"]
)
@admin_only
def delete_report(report_id: str):
    """ """
    report = get_obj(Report, report_id)
    if not report:
        abort(404, description="Report does not exist.")

    db = DatabaseOp()
    db.delete(report)
    db.commit()
    return jsonify({}), 200
