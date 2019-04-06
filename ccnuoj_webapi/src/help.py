from flask import g

from .util import http, get_request_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Contest, User
from .authentication import require_authentication


@bp.route("/help/predict/<string:id>", methods=["GET"])
def retrieve_help_predict(id):
    result = []
    result.append({'id':id, 'user':'wzq', 'status':'pass', 'probability':0.8})
    instance = {
        "result": result,
    }
    return http.Success(result=instance)
