import datetime
from flask import g

from .util import to_json
from .global_obj import database as db
from .model import Submission
from .model import JudgeCommand
from .model import JudgeRequest, JudgeState


def auto_create_for_submission(submission: Submission) -> JudgeRequest:
    current_datetime = datetime.datetime.now()

    judge_command = JudgeCommand()
    judge_command.operator = g.user.id
    judge_command.createTime = current_datetime
    judge_command.command = to_json({}) # !!stub
    db.session.add(judge_command)
    db.session.flush()

    judge_request = JudgeRequest()
    judge_request.submission = submission.id
    judge_request.operator = g.user.id
    judge_request.reason = "Auto created for submission"
    judge_request.createTime = current_datetime
    judge_request.state = JudgeState.pending
    judge_request.judgeCommand = judge_command.id
    db.session.add(judge_request)
    db.session.flush()

    return judge_request
