import datetime
from flask import g

from .util import http, get_request_json, to_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Submission
from .model import JudgeRequest, JudgeState
from .authentication import require_authentication
from . import judge_command


def auto_create_for_submission(submission: Submission) -> JudgeRequest:
    current_datetime = datetime.datetime.now()

    judge_request = JudgeRequest()
    judge_request.submission = submission.id
    judge_request.operator = g.user.id
    judge_request.reason = "Auto created for submission"
    judge_request.createTime = current_datetime
    judge_request.state = JudgeState.waiting
    db.session.add(judge_request)
    db.session.flush()

    judge_command.auto_create_for_submission(submission, judge_request)

    return judge_request


@bp.route("/judge_request/id/<int:id>/state", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def update_judge_request_state(id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "update the state of a judge request",
        "type": "object",
        "properties": {
            "value": {
                "type": "string"
            }
        },
        "required": ["value"],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)
    value = instance["value"]
    if value in JudgeState.__members__:
        judge_request = JudgeRequest.query.get(id)
        if judge_request is None:
            raise http.NotFound(body={
                "status": "Failed",
                "reason": "JudgeRequestNotFound"
            })
        else:
            if judge_request.finishTime is None:
                old_state = judge_request.state
                judge_request.state = JudgeState[value]
                db.session.commit()
                return to_json({
                    "status": "Success",
                    "oldState": old_state.name
                })
            else:
                raise http.Conflict({
                    "status": "Failed",
                    "reason": "JudgeRequestAlreadyFinished",
                    "finishTime": judge_request.finishTime
                })
    else:
        raise http.BadRequest(body={
            "status": "Failed",
            "reason": "UnrecognizedJudgeState"
        })


@bp.route("/judge_request/id/<int:id>/finished", methods=["POST"])
@require_authentication(allow_anonymous=False)
def mark_judge_request_finished(id: int):
    judge_request = JudgeRequest.query.get(id)
    if judge_request is None:
        raise http.NotFound(body={
            "status": "Failed",
            "reason": "JudgeRequestNotFound"
        })
    else:
        if judge_request.finishTime is None:
            judge_request.finishTime = g.request_datetime
            db.session.commit()
            return to_json({
                "status": "Success",
                "finishTime": judge_request.finishTime
            })
        else:
            raise http.Gone({
                "status": "Failed",
                "reason": "JudgeRequestAlreadyFinished",
                "finishTime": judge_request.finishTime
            })