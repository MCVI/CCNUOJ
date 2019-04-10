from flask import g

from .util import get_request_json
from .util import http
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Problem, User
from .authentication import require_authentication
from .authorization import require_super
from .judge_scheme import judge_scheme_dict, JudgeSchemeNotFound, JudgeScheme


def get_judge_scheme_by_name(name: str) -> JudgeScheme:
    try:
        judge_scheme = judge_scheme_dict[name]
    except JudgeSchemeNotFound:
        raise http.NotFound(reason="JudgeSchemeNotFound")

    return judge_scheme


@bp.route("/problem", methods=["POST"])
@require_super
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

    judge_scheme = get_judge_scheme_by_name(instance["judgeScheme"])

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
        "problemID": problem.id,
        "createTime": problem.createTime,
    })


@bp.route("/problem/id/<int:problem_id>", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def update_problem(problem_id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "update a existing problem",
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
        "required": [],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)

    problem = Problem.query.get(problem_id)
    if problem is None:
        raise http.NotFound(reason="ProblemNotFound")
    if not ((g.user.id == problem.author) or g.user.isSuper):
        raise http.Forbidden(reason="PermissionDenied")

    for key in ["title", "text", "extraInfo"]:
        if key in instance:
            value = instance[key]
            setattr(problem, key, value)

    if "judge_scheme" in instance:
        judge_scheme = get_judge_scheme_by_name(instance["judgeScheme"])
        problem.judgeScheme = judge_scheme.short_name
    else:
        judge_scheme = get_judge_scheme_by_name(problem.judgeScheme)

    if "limitInfo" in instance:
        try:
            judge_scheme.validate_limit_info(instance["limitInfo"])
        except judge_scheme.ValidationError as e:
            raise http.BadRequest(
                reason="InvalidLimitInfo",
                detail=e.detail
            )
        problem.limitInfo = instance["limitInfo"]

    problem.lastModifiedTime = g.request_datetime

    db.session.add(problem)
    db.session.commit()

    return http.Success({
        "lastModifiedTime": problem.lastModifiedTime,
    })


@bp.route("/problem/id/<int:id>", methods=["DELETE"])
def delete_problem(id: int):
    pass


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


@bp.route("/problem/page/<int:page_num>", methods=["GET"])
def get_problem_list(page_num: int):
    problem_list = Problem.query.paginate(
        page=page_num,
        per_page=20
    ).items

    instance = []
    for problem in problem_list:
        author: User = User.query.get(problem.author)

        inst = {
            "id": problem.id,
            "title": problem.title,
            "author": {
                "id": author.id,
                "shortName": author.shortName,
            },
            "createTime": problem.createTime,
            "lastModifiedTime": problem.lastModifiedTime,
        }

        instance.append(inst)

    return http.Success(result=instance)
