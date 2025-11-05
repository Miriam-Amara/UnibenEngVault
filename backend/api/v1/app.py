#!/usr/bin/env python3

"""

"""

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt # type: ignore
from flask_cors import CORS
from flask import Flask, g, request, abort
from typing import Optional
import os
import sys
import traceback

from api.v1.views import app_views
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.utils.error_handlers import (
    bad_request, not_found, conflict_error, large_request_error,
    method_not_allowed, forbidden, unauthorized, server_error
)
from models import storage
from models.user import User

from api.v1.views.users import create_first_user
from models.user import User


load_dotenv()
bcrypt = Bcrypt()
auth = SessionDBAuth()

ALLOWED_ORIGINS = [
            "https://uniben-eng-vault.vercel.app",
            "http://localhost:5173"
        ]
def verify_auth():
    """ """
    if request.method == 'OPTIONS':
        return  # Allow the OPTIONS request to proceed unauthenticated

    if not auth.require_auth(
        request.path,
        [
            "/api/v1/stats/", "/api/v1/register/",
            "/api/v1/auth_session/login/",
            f"/api/v1/departments/{13}/{1}",
            f"/api/v1/levels/{13}/{1}"
        ]
    ):
        return
    
    if not auth.session_cookie():
        abort(401)
    
    user: User | None = auth.current_user()
    if not user:
        abort(401)
    g.current_user = user

def close_db(exception: Optional[BaseException]) -> None:
    """
    """
    storage.close()


def create_app(config_name: str | None=None) -> Flask:
    """
    """
    app = Flask(__name__)
    
    if config_name == "test":
        app.config.from_mapping(TESTING=True)
    else:
        app.config.from_mapping(TESTING=False)
    
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024 * 1024
    bcrypt.init_app(app) # type: ignore
    CORS(
        app,
        resources={r"/api/v1/*": {"origins": ALLOWED_ORIGINS,
        }},
        allow_headers=["Content-Type", "Authorization", "X-Custom-Header"],
        supports_credentials=True
    )
    app.register_blueprint(app_views)
    app.before_request(verify_auth)
    app.teardown_appcontext(close_db)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(409, conflict_error)
    app.register_error_handler(413, large_request_error)
    app.register_error_handler(500, server_error)

    if storage.count(User) == 0:
        create_first_user()

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        # This forces the full traceback to print to the console
        traceback.print_exc(file=sys.stderr)

        # Return a generic response to the browser
        return "An internal server error occurred. Check server logs for details.", 500

    @app.after_request
    def force_cors_headers(response):
        # 1. Get the origin from the request headers
        origin = request.headers.get('Origin')

        # 2. Check if the requesting origin is in our allowed list
        if origin and origin in ALLOWED_ORIGINS:
            # 3. CRITICAL: Set the mandatory credentialed CORS headers
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'

        return response

    return app


config_name = os.getenv("ENV", "development")
app = create_app(config_name)


if __name__ == "__main__":
    host = os.getenv("UNIBENENGVAULT_API_HOST", "0.0.0.0")
    port = int(os.getenv("UNIBENENGVAULT_API_PORT", 5000))
    debug_mode = bool(os.getenv("DEBUG_MODE", False))
    app.run(host=host, port=port, threaded=True, debug=debug_mode)
