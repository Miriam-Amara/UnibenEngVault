#!/usr/bin/env python3

"""

"""

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt # type: ignore
from flask import Flask
from typing import Optional
from werkzeug.exceptions import HTTPException
import os

from api.v1.views import app_views
from models import storage


load_dotenv()

app = Flask(__name__)
app.register_blueprint(app_views)
bcrypt = Bcrypt(app)

@app.teardown_appcontext
def close_db(exception: Optional[BaseException]) -> None:
    storage.close()

@app.errorhandler(404)
def not_found(error: HTTPException):
    """Handles 404 request errors"""
    if error.description:
        return {"msg": error.description}
    return {"Error": "Not found"}, 404

@app.errorhandler(400)
def bad_request(error: HTTPException):
    """Handles 400 bad request errors"""
    return {"message": error.description}, 400

@app.errorhandler(500)
def server_error(error: HTTPException):
    """Handles 500 server request errors"""
    return {"message": error.description}, 500


if __name__ == "__main__":
    host = os.getenv("UNIBENENGVAULT_API_HOST", "0.0.0.0")
    port = int(os.getenv("UNIBENENGVAULT_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
