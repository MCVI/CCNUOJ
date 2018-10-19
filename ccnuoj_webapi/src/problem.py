from flask import g

from .util import get_request_json, to_json
from .util import http
from . import model
from .model import Problem
from .global_obj import database as db
from .global_obj import blueprint as bp
from .authentication import require_authentication
from . import judge_scheme


@bp.route("/problem", methods=["POST"])
@require_authentication(allow_anonymous=False)
def create_problem():
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "create a new problem",
        "type": "object",
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
            "judgeSchemeShortName": {
                "type": "string"
            },
            "limitInfo": {
                "type": "object"
            },
        },
        "required": ["title", "text", "extraInfo", "limitInfo"],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)
    judge_scheme_short_name = instance["judgeSchemeShortName"]

    judge_scheme_rec = model.JudgeScheme.query.filter_by(shortName=judge_scheme_short_name).first()
    if judge_scheme_rec is None:
        raise http.NotFound(body={
            "status": "Failed",
            "reason": "JudgeSchemeNotFound"
        })

    try:
        judge_scheme_cls = judge_scheme.get(judge_scheme_short_name)
    except judge_scheme.SchemeNotFound:
        raise http.NotImplemented(body={
            "status": "Failed",
            "reason": "JudgeSchemeNotImplemented"
        })

    try:
        judge_scheme_cls.validate_limit_info(instance["limitInfo"])
    except judge_scheme.ValidationError as e:
        raise http.BadRequest(body={
            "status": "Failed",
            "reason": "InvalidLimitInfo",
            "detail": e.detail
        })

    problem = Problem()
    for key in ["title", "text", "extraInfo", "judgeScheme", "judgeParam", "limitInfo"]:
        value = instance[key]
        setattr(problem, key, value)

    problem.author = g.user.id
    problem.createTime = g.request_datetime
    problem.lastModifiedTime = g.request_datetime

    db.session.add(problem)
    db.session.commit()

    return to_json({
        "status": "Success",
        "problemID": problem.id
    })


@bp.route("/problem/id/<int:id>", methods=["GET"])
def get_problem(id: int):
    problem = Problem.query.get(id)

    if problem is None:
        raise http.NotFound(body={
            "status": "Failed",
            "reason": "ProblemNotFound"
        })
    else:
        instance = {}
        for key in ["title", "text", "extraInfo", "judgeScheme", "limitInfo", "createTime", "lastModifiedTime"]:
            value = getattr(problem, key)
            instance[key] = value

        instance["authorID"] = problem.author

        return to_json({
            "status": "Success",
            "result": instance
        })


@bp.route("/problem/id/<int:id>", methods=["PUT"])
def update_problem(id: int):
    pass


@bp.route("/problem/id/<int:id>", methods=["DELETE"])
def delete_problem(id: int):
    pass
