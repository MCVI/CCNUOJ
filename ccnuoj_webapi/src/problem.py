from flask import g

from .util import get_request_json, to_json
from .model import Problem
from .global_obj import database as db
from .global_obj import blueprint as bp
from .authentication import require_authentication


@bp.route("/problem", methods=["POST"])
@require_authentication(allow_anonymous=False)
def create_problem():
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "create a new problem",
        "properties": {
            "title": {
                "type": "string"
            },
            "text": {
                "type": "string"
            },
            "extraInfo": {
                "type": "object"
            },
            "limitInfo": {
                "type": "object"
            },
            "judgeScheme": {
                "type": "number"
            },
            "judgeParam": {
                "type": "object"
            }
        },
        "required": ["title", "text", "extraInfo", "limitInfo", "judgeScheme", "judgeParam"]
    }
    instance = get_request_json(schema=schema)

    # validate judgeParam with judgeScheme

    problem = Problem()
    for key in ["title", "text", "extraInfo"]:
        value = instance[key]
        setattr(problem, key, value)

    problem.author = g.user
    problem.createTime = g.request_datetime
    problem.lastModifiedTime = g.request_datetime

    db.session.add(problem)
    db.session.commit()

    return to_json({
        "status": "Success"
    })


@bp.route("/problem/id/<int:id>", methods=["GET"])
def get_problem(id: int):
    pass


@bp.route("/problem/id/<int:id>", methods=["PUT"])
def update_problem(id: int):
    pass


@bp.route("/problem/id/<int:id>", methods=["DELETE"])
def delete_problem(id: int):
    pass
