from flask import g

from .util import get_request_json
from .util import http
from .model import Problem
from .global_obj import database as db
from .global_obj import blueprint as bp
from .authentication import require_authentication
from .judge_scheme import judge_scheme_dict, JudgeSchemeNotFound


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
            "judgeScheme": {
                "type": "string"
            },
            "limitInfo": {
                "type": "object"
            },
        },
        "required": ["title", "text", "extraInfo", "limitInfo", "judgeScheme"],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)

    try:
        judge_scheme = judge_scheme_dict[instance["judgeScheme"]]
    except JudgeSchemeNotFound:
        raise http.NotFound(reason="JudgeSchemeNotFound")

    try:
        judge_scheme.validate_limit_info(instance["limitInfo"])
    except judge_scheme.ValidationError as e:
        raise http.BadRequest(
            reason="InvalidLimitInfo",
            detail=e.detail
        )

    problem = Problem()
    for key in ["title", "text", "extraInfo", "limitInfo"]:
        value = instance[key]
        setattr(problem, key, value)

    problem.judgeScheme = judge_scheme.short_name
    problem.author = g.user.id
    problem.createTime = g.request_datetime
    problem.lastModifiedTime = g.request_datetime

    db.session.add(problem)
    db.session.commit()

    return http.Success({
        "problemID": problem.id
    })


@bp.route("/problem/id/<int:id>", methods=["GET"])
def get_problem(id: int):
    problem = Problem.query.get(id)

    if problem is None:
        raise http.NotFound(reason="ProblemNotFound")
    else:
        instance = {}
        for key in ["title", "text", "extraInfo", "limitInfo", "createTime", "lastModifiedTime"]:
            value = getattr(problem, key)
            instance[key] = value

        judge_scheme = judge_scheme_dict[problem.judgeScheme]
        instance["judgeScheme"] = judge_scheme.short_name
        instance["authorID"] = problem.author

        return http.Success(result=instance)


@bp.route("/problem/id/<int:id>", methods=["PUT"])
def update_problem(id: int):
    pass


@bp.route("/problem/id/<int:id>", methods=["DELETE"])
def delete_problem(id: int):
    pass
