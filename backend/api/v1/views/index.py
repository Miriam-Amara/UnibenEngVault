#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify

from api.v1.views import app_views
from models import storage


@app_views.route("/stats", strict_slashes=True, methods=["GET"])
def index():
    """
    
    """
    objects_count = storage.count()
    if not objects_count:
        abort(404)
    return jsonify(objects_count), 200

