from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, g
import datetime

database = SQLAlchemy()

blueprint = Blueprint("main", __name__)


@blueprint.before_app_request
def record_request_info():
    g.request_datetime = datetime.datetime.now()
