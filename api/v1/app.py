#!/usr/bin/env python3

"""

"""

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt # type: ignore
from flask_cors import CORS
from flask import Flask, g, request, abort, current_app
from typing import Optional, cast
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge
import os

from api.v1.views import app_views
from api.v1.auth.session_db_auth import SessionDBAuth
from models.engine.db_storage import DBStorage


load_dotenv()


class MyFlask(Flask):
    """Prevents pylance error."""
    storage: DBStorage

def create_app(config_name: str | None=None) -> MyFlask:
    """
    """
    app = MyFlask(__name__)
    
    if config_name == "testing":
        app.config.from_mapping(
            DATABASE_URL= os.getenv("DATABASE_URL_TEST"),
            TESTING=True
        )
    elif config_name == "production":
        app.config.from_mapping(
            DATABASE_URL=os.getenv("DATABASE_URL_PRO"),
            TESTING=False
        )
    else:
        app.config.from_mapping(
            DATABASE_URL=os.getenv("DATABASE_URL_DEV"),
            TESTING=False
        )

    database_url: str = cast(str, app.config["DATABASE_URL"])
    app.storage = DBStorage(database_url)
    app.storage.reload()
    
    return app

app = create_app()
app.register_blueprint(app_views)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", 3600))
bcrypt = Bcrypt(app)

CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

auth = SessionDBAuth()

@app.before_request
def verify_auth():
    """ """
    if not auth.require_auth(
        request.path,
        [
            "/api/v1/stats/", "/api/v1/register/",
            "/api/v1/auth_session/login/"
        ]
    ):
        return
    if not auth.authorization_header(request):
        abort(401)

    if auth.authorization_header(request) and not auth.session_cookie(request):
        abort(401)
    
    user = auth.current_user(request)
    if not user:
        abort(403)
    g.current_user = user

@app.teardown_appcontext
def close_db(exception: Optional[BaseException]) -> None:
    """
    """
    app = cast(MyFlask, current_app)
    app.storage.close()

@app.errorhandler(400)
def bad_request(error: HTTPException):
    """Handles 400 bad request errors"""
    if error.description:
        return {"error": error.description}, 400
    return {"error": "bad request"}, 400

@app.errorhandler(401)
def unauthorized(error: HTTPException):  
    return {"error": "Unauthorized"}, 401

@app.errorhandler(403)
def forbidden(error: HTTPException):
    return {"error": "Forbidden"}, 403

@app.errorhandler(404)
def not_found(error: HTTPException):
    """Handles 404 request errors"""
    if error.description:
        return {"error": error.description}, 404
    return {"Error": "Not found"}, 404

@app.errorhandler(405)
def method_not_allowed(error: HTTPException):
    """Handles 405 request errors"""
    if error.description:
        return {"error": error.description}, 405
    return {"Error": "Method not allowed"}, 405

@app.errorhandler(409)
def conflict_error(error: HTTPException):
    """Handles data conflict errors"""
    return {"error": error.description}, 409

@app.errorhandler(500)
def server_error(error: HTTPException):
    """Handles 500 server request errors"""
    return {"error": "Internal Server Error"}, 500

@app.errorhandler(413)
def large_request_error(error: RequestEntityTooLarge):
    """Handles files too large errors"""
    return {"error": "File too large! Max upload size is 1GB."}, 413


if __name__ == "__main__":
    host = os.getenv("UNIBENENGVAULT_API_HOST", "0.0.0.0")
    port = int(os.getenv("UNIBENENGVAULT_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
