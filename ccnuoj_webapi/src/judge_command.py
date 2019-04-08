import datetime
from flask import g

from .util import get_request_json
from .util import http
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import JudgeCommand, JudgeRequest
from .authentication import require_authentication
from .authorization import require_super


def create_for_judge_request(
        judge_request: JudgeRequest
) -> JudgeCommand:
    current_datetime = datetime.datetime.now()

    command = JudgeCommand()
    command.operator = g.user.id
    command.judgeRequest = judge_request.id
    command.createTime = current_datetime
    command.fetched = False

    command.command = {
        "type": "JudgeRequest",
        "judgeRequestID": judge_request.id,
    }

    db.session.add(command)
    db.session.flush()

    return command


@bp.route("/judge_command/fetched/all", methods=["GET"])
@require_super
def get_fetched_command():
    commands = (
        JudgeCommand.query
        .filter(db.and_(
            JudgeCommand.fetchTime!=None,
            JudgeCommand.finishTime==None
        ))
        .order_by(JudgeCommand.createTime.asc())
        .all()
    )

    result = []
    for command in commands:
        obj = {}
        for key in ["id", "operator", "createTime", "fetchTime", "command"]:
            obj[key] = getattr(command, key)
        result.append(obj)

    return http.Success(result=result)


@bp.route("/judge_command/unfetched/<int:limit>", methods=["GET"])
@require_super
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
        for key in ["id", "operator", "createTime", "fetchTime", "command"]:
            obj[key] = getattr(command, key)
        result.append(obj)

    return http.Success(result=result)


@bp.route("/judge_command/<int:id>/fetched", methods=["POST"])
@require_super
def mark_command_fetched(id: int):
    command = JudgeCommand.query.get(id)

    if command is None:
        raise http.NotFound(reason="JudgeCommandNotFound")
    else:
        if command.fetchTime is None:
            command.fetchTime = g.request_datetime
            db.session.commit()
            return http.Success(fetchTime=command.fetchTime)
        else:
            raise http.Gone(
                reason="JudgeCommandAlreadyFetched",
                detail={
                    "fetchTime": command.fetchTime
                }
            )


@bp.route("/judge_command/<int:id>/finished", methods=["POST"])
@require_super
def mark_command_finished(id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "mark a command as finished",
        "type": "object",
        "properties": {
            "result": {
                "oneOf": [
                    {
                        "type": "null",
                    },
                    {
                        "type": "object",
                    }
                ]
            }
        },
        "required": ["result"],
        "additionalProperties": False
    }
    instance = get_request_json(schema)

    command = JudgeCommand.query.get(id)
    if command is None:
        raise http.NotFound(reason="JudgeCommandNotFound")
    elif command.fetchTime is None:
        raise http.Conflict(reason="JudgeCommandNotFetched")
    elif command.finishTime is not None:
        raise http.Gone(
            reason="JudgeCommandAlreadyFinished",
            detail={
                "finishTime": command.finishTime
            }
        )
    else:
        command.finishTime = g.request_datetime
        command.result = instance["result"]

        request = JudgeRequest.query.get(command.judgeRequest)
        request.finishTime = g.request_datetime

        db.session.commit()
        return http.Success(finishTime=request.finishTime)
