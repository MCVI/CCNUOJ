import datetime
from flask import g

from .global_obj import database as db
from .model import Submission
from .model import JudgeRequest, JudgeState
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
