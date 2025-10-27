#!/usr/bin/env python3

"""
"""


from flask import jsonify
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge

def bad_request(error: HTTPException):
    """Handles 400 bad request errors"""
    if error.description:
        return jsonify({"error": error.description}), 400
    return jsonify({"error": "bad request"}), 400

def unauthorized(error: HTTPException):
    """Handles 401 unauthorized request errors"""
    return jsonify({"error": "Unauthorized"}), 401

def forbidden(error: HTTPException):
    """Handles 403 forbidden request errors"""
    return jsonify({"error": "Forbidden"}), 403

def not_found(error: HTTPException):
    """Handles 404 request errors"""
    if error.description:
        return jsonify({"error": error.description}), 404
    return jsonify({"Error": "Not found"}), 404

def method_not_allowed(error: HTTPException):
    """Handles 405 request errors"""
    if error.description:
        return jsonify({"error": error.description}), 405
    return jsonify({"Error": "Method not allowed"}), 405

def conflict_error(error: HTTPException):
    """Handles 409 data conflict errors"""
    return jsonify({"error": error.description}), 409

def server_error(error: HTTPException):
    """Handles 500 server request errors"""
    return jsonify({"error": "Internal Server Error"}), 500

def large_request_error(error: RequestEntityTooLarge):
    """Handles files too large errors"""
    return jsonify({"error": "File too large! Max upload size is 1GB."}), 413

