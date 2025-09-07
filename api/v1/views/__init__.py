#!/usr/bin/env python3

"""

"""


from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


from api.v1.views.admins import *
from api.v1.views.courses import *
from api.v1.views.departments import *
from api.v1.views.feedbacks import *
from api.v1.views.files import *
from api.v1.views.helps import *
from api.v1.views.index import *
from api.v1.views.levels import *
from api.v1.views.notifications import *
from api.v1.views.reports import *
from api.v1.views.tutorial_links import *
from api.v1.views.users import *