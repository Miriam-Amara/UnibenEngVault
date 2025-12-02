#!/usr/bin/env python3

"""
Implements /stats route for retrieving the count
of all class objects in the database.
"""


from flask import abort, jsonify

from api.v1.views import app_views
from models import storage


@app_views.route("/stats", strict_slashes=True, methods=["GET"])
def index():
    """
    Returns the count of all class objects in the database.
    """
    objects_count = storage.count()
    if not objects_count:
        abort(404)
    return jsonify(objects_count), 200
