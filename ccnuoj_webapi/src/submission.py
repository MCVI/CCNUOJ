from flask import g

from .util import get_request_json
from .util import http
from .util import pagination_list
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Submission, Problem, User, JudgeRequest
from .authentication import require_authentication
from .judge_request import auto_create_for_submission
from .language import language_dict, LanguageNotFound
from .judge_scheme import judge_scheme_dict


@bp.route("/submission", methods=["POST"])
@require_authentication(allow_anonymous=False)
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


@bp.route("/submission/page/<int:page_num>", methods=["GET"])
@require_authentication(allow_anonymous=True)
def get_submission_list(page_num: int):
    submission_list = pagination_list(Submission.query, page=page_num)

    instance_list = []
    for submission in submission_list.items:
        problem: Problem = Problem.query.get(submission.problem)
        contest = None  # not implemented
        author: User = User.query.get(submission.author)
        latest_judge_request: JudgeRequest = (
            JudgeRequest
                .query
                .filter_by(submission=submission.id)
                .order_by(JudgeRequest.createTime.desc())
                .limit(1)
                .first()
        )

        instance = {
            "id": submission.id,
            "createTime": submission.createTime,
            "problem": {
                "id": submission.problem,
                "title": problem.title,
            },
            "contest": contest,
            "author": {
                "id": author.id,
                "shortName": author.shortName,
            },
            "language": submission.language,
            "latestJudgeRequest": {
                "id": latest_judge_request.id,
                "state": latest_judge_request.state.value,
            },
        }
        instance_list.append(instance)

    return http.Success(result={
        "page_count": submission_list.pages,
        "list": instance_list,
    })
