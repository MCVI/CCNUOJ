import datetime
from flask import g

from .util import get_request_json, to_json
from .util import http
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import JudgeCommand, JudgeRequest, JudgeScheme
from .model import Submission, Problem, Language
from .authentication import require_authentication


def auto_create_for_submission(
        submission: Submission,
        judge_request: JudgeRequest
) -> JudgeCommand:
    current_datetime = datetime.datetime.now()

    command = JudgeCommand()
    command.operator = g.user.id
    command.judgeRequest = judge_request.id
    command.createTime = current_datetime
    command.fetched = False

    problem = Problem.query.get(submission.problem)
    judge_scheme = JudgeScheme.query.get(problem.judgeScheme)
    language = Language.query.get(submission.language)

    command.command = {
        "type": "CodeJudge",
        "judgeRequest": judge_request.id,
        "judgeSchemeShortName": judge_scheme.shortName,
        "language": language.shortName,
        "code": submission.text
    }

    db.session.add(command)
    db.session.flush()

    return command


@bp.route("/judge_command/unfetched/<int:limit>", methods=["GET"])
@require_authentication(allow_anonymous=False)
def get_unfetched_command(limit: int):
    commands = (
        JudgeCommand.query
        .filter_by(fetchTime=None)
        .order_by(JudgeCommand.createTime.asc())
        .limit(limit)
        .all()
    )

    result = []
    for command in commands:
        obj = {}
        for key in ["id", "operator", "createTime", "command"]:
            obj[key] = getattr(command, key)
        result.append(obj)

    return to_json({
        "status": "Success",
        "result": result
    })


@bp.route("/judge_command/<int:id>/fetched", methods=["POST"])
@require_authentication(allow_anonymous=False)
def mark_command_fetched(id: int):
    command = JudgeCommand.query.get(id)

    if command is None:
        raise http.NotFound(body={
            "status": "Failed",
            "reason": "JudgeCommandNotFound"
        })
    else:
        if command.fetchTime is None:
            command.fetchTime = g.request_datetime
            db.session.commit()
            return to_json({
                "status": "Success",
                "fetchTime": command.fetchTime
            })
        else:
            raise http.Gone(body={
                "status": "Failed",
                "reason": "JudgeCommandAlreadyFetched",
                "detail": {
                    "fetchTime": command.fetchTime
                }
            })


@bp.route("/judge_command/<int:id>/finished", methods=["POST"])
@require_authentication(allow_anonymous=False)
def mark_command_finished(id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "mark a command as finished",
        "type": "object",
        "properties": {
            "result": {
                "type": "object"
            }
        },
        "required": ["result"],
        "additionalProperties": False
    }
    instance = get_request_json(schema)

    command = JudgeCommand.query.get(id)
    if command is None:
        raise http.NotFound(body={
            "status": "Failed",
            "reason": "JudgeCommandNotFound"
        })
    elif command.fetchTime is None:
        raise http.Conflict(body={
            "status": "Failed",
            "reason": "JudgeCommandNotFetched"
        })
    elif command.finishTime is not None:
        raise http.Gone(body={
            "status": "Failed",
            "reason": "JudgeCommandAlreadyFinished",
            "finishTime": command.finishTime
        })
    else:
        command.finishTime = g.request_datetime
        command.result = instance["result"]

        request = JudgeRequest.query.get(command.judgeRequest)
        request.finishTime = g.request_datetime

        db.session.commit()
        return to_json({
            "status": "Success",
            "finishTime": request.finishTime
        })
