from flask import g

from .util import get_request_json
from .util import http
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Submission, Problem
from .authentication import require_authentication
from .judge_request import auto_create_for_submission
from .language import language_dict, LanguageNotFound
from .judge_scheme import judge_scheme_dict


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
            "language": {
                "type": "string"
            },
            "text": {
                "type": "string"
            }
        },
        "required": ["problemID", "text", "language"],
        "additionalProperties": False
    }
    instance = get_request_json(schema=schema)

    submission = Submission()
    submission.problem = instance["problemID"]
    if "contestID" in instance:
        contest_id = instance["contestID"]
        if contest_id is not None:
            submission.contest = contest_id
            raise http.NotImplemented(reason="ContestNotImplemented")
    try:
        language = language_dict[instance["language"]]
    except LanguageNotFound:
        raise http.NotFound(reason="LanguageNotFound")
    submission.language = language.short_name

    problem = Problem.query.get(instance["problemID"])
    judge_scheme = judge_scheme_dict[problem.judgeScheme]
    if language.short_name not in judge_scheme.supported_language:
        raise http.Conflict(
            reason="LanguageNotSupportedByJudgeScheme",
            detail={
                "supportedLanguage": judge_scheme.supported_language
            }
        )

    submission.text = instance["text"]
    submission.createTime = g.request_datetime
    submission.author = g.user.id

    db.session.add(submission)
    db.session.flush()

    judge_request = auto_create_for_submission(submission)

    db.session.commit()
    return http.Success({
        "submissionID": submission.id,
        "judgeRequestID": judge_request.id
    })
