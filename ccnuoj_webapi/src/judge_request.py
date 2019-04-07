import datetime
from flask import g

from .util import http, get_request_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Submission
from .model import JudgeRequest, JudgeState
from .authentication import require_authentication
from .authorization import require_super
from . import judge_command


def auto_create_for_submission(submission: Submission) -> JudgeRequest:
    current_datetime = datetime.datetime.now()

    judge_request = JudgeRequest()
    judge_request.submission = submission.id
    judge_request.operator = g.user.id
    judge_request.reason = "Auto created for submission"
    judge_request.createTime = current_datetime
    judge_request.state = JudgeState.waiting
    judge_request.detail = None
    db.session.add(judge_request)
    db.session.flush()

    judge_command.create_for_judge_request(judge_request)

    return judge_request


@bp.route("/judge_request/id/<int:id>/state", methods=["PUT"])
@require_super
def update_judge_request_state(id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "update the state of a judge request",
        "type": "object",
        "properties": {
            "state": {
                "type": "string"
            },
            "detail": {
                "type": "object"
            }
        },
        "required": ["state"],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)
    state = instance["state"]
    if state in JudgeState.__members__:
        judge_request = JudgeRequest.query.get(id)
        if judge_request is None:
            raise http.NotFound(reason="JudgeRequestNotFound")
        else:
            if judge_request.finishTime is None:
                old_state = judge_request.state
                judge_request.state = JudgeState[state]
                judge_request.detail = instance["detail"]
                db.session.commit()
                return http.Success({
                    "oldState": old_state.name,
                })
            else:
                raise http.Conflict(
                    reason="JudgeRequestAlreadyFinished",
                    detail={
                        "finishTime": judge_request.finishTime
                    }
                )
    else:
        raise http.BadRequest(reason="UnrecognizedJudgeState")


@bp.route("/judge_request/id/<int:id>/finished", methods=["POST"])
@require_super
def mark_judge_request_finished(id: int):
    judge_request = JudgeRequest.query.get(id)
    if judge_request is None:
        raise http.NotFound(reason="JudgeRequestNotFound")
    else:
        if judge_request.finishTime is None:
            judge_request.finishTime = g.request_datetime
            db.session.commit()
            return http.Success(finishTime=judge_request.finishTime)
        else:
            raise http.Gone(
                reason="JudgeRequestAlreadyFinished",
                detail={
                    "finishTime": judge_request.finishTime
                }
            )


@bp.route("/judge_request/id/<int:id>", methods=["GET"])
@require_authentication(allow_anonymous=False)
def retrieve_judge_request(id: int):
    judge_request = JudgeRequest.query.get(id)
    if judge_request is None:
        raise http.NotFound(reason="JudgeRequestNotFound")
    else:
        if g.user.isSuper or (g.user.id == judge_request.operator):
            return http.Success(result={
                "id": judge_request.id,
                "submission": judge_request.submission,
                "operator": judge_request.operator,
                "reason": judge_request.reason,
                "createTime": judge_request.createTime,
                "finishTime": judge_request.finishTime,
                "state": judge_request.state.value,
                "detail": judge_request.detail,
            })
        else:
            raise http.Forbidden(reason="PermissionDenied")
