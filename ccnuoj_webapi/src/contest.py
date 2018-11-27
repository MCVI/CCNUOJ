from flask import g

from .util import http, get_request_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Contest, User
from .authentication import require_authentication


@bp.route("/contest/id/<int:id>", methods=["GET"])
def retrieve_contest(id: int):
    contest = Contest.query.get(id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")

    author: User = User.query.get(contest.author)
    instance = {
        "id": contest.id,
        "needRegister": contest.needRegister,

        "title": contest.title,
        "text": contest.text,
        "extraInfo": contest.extraInfo,

        "author": {
            "id": author.id,
            "shortName": author.shortName,
        },

        "startTime": contest.startTime,
        "endTime": contest.endTime,

        "freezeTime": contest.freezeTime,
        "unfreezeTime": contest.unfreezeTime,

        "createTime": contest.createTime,
        "lastModifiedTime": contest.lastModifiedTime,
    }

    return http.Success(result=instance)


@bp.route("/contest/list", methods=["GET"])
def retrieve_contest_list():
    contest_list = Contest.query.all()

    instance = []
    for contest in contest_list:
        author: User = User.query.get(contest.author)

        inst = {
            "id": contest.id,
            "needRegister": contest.needRegister,

            "title": contest.title,
            "author": {
                "id": author.id,
                "shortName": author.shortName,
            },

            "startTime": contest.startTime,
            "endTime": contest.endTime,
        }

        instance.append(inst)

    return http.Success(result=instance)


@bp.route("/contest/id/<int:id>/text", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def update_contest_text(id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "update the text of a contest",
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
            },
        },
        "required": ["text"],
        "additionalProperties": False,
    }
    instance = get_request_json(schema=schema)

    contest: Contest = Contest.query.get(id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")

    if contest.author == g.user.id or g.user.isSuper:
        contest.text = instance["text"]
        contest.lastModifiedTime = g.request_datetime

        db.session.commit()
        return http.Success(result={
            "lastModifiedTime": contest.lastModifiedTime,
        })
    else:
        raise http.Forbidden(reason="PermissionDenied")
