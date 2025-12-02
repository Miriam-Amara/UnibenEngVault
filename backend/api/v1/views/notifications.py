# #!/usr/bin/env python3

# """

# """


# from flask import jsonify, g
# from typing import cast
# import logging

# from api.v1.views import app_views

# # from api.v1.auth.authorization import admin_only
# # from api.v1.utils import get_obj
# # from api.v1.data_validations import DatabaseOp
# # from models import storage
# # from models.admin import Admin
# # from models.course import Course
# # from models.department import Department
# # from models.notification import Notification
# # from models.user import User


# logger = logging.getLogger(__name__)


# # @app_views.route(
# # "/notifications", strict_slashes=False, methods=["GET"]
# # )
# # def get_notifications():
# #     """ """
# #     user = cast(User, g.current_user)
# #     notifications = Notification.get_notifications(user)
# #     logger.debug(notifications)
# #     return jsonify(notifications), 200
