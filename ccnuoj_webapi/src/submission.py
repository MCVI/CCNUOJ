from flask import g

from .util import get_request_json, to_json
from .global_obj import blueprint as bp
from .global_obj import database as db
from .model import Submission
from .authentication import require_authentication
from .judge_request import auto_create_for_submission


@bp.route("/submission", methods=["POST"])
@require_authentication()
def create_submission():
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "create submission of a problem",
        "type": "object",
        "properties": {
            "problemID": {
                "type": "number"
            },
            "contestID": {
                "comment": "optional",
                "type": "null"
            },
            "text": {
                "type": "string"
            }
        },
        "required": ["problemID", "text"],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)

    submission = Submission()
    submission.problem = instance["problemID"]
    if "contestID" in instance:
        contest_id = instance["contestID"]
        if contest_id is not None:
            submission.contest = contest_id

    submission.text = instance["text"]

    submission.createTime = g.request_datetime
    submission.author = g.user.id

    db.session.add(submission)
    db.session.flush()

    judge_request = auto_create_for_submission(submission)

    db.session.commit()
    return to_json({
        "status": "Success",
        "submissionID": submission.id,
        "judgeRequestID": judge_request.id
    })
