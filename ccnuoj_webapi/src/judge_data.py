from flask import request, g

from .util import http
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Problem, JudgeData
from .authentication import require_authentication
from .judge_scheme import judge_scheme_dict, ValidationError


# Notice: The request body is not supposed to be json
@bp.route("/problem/id/<int:problem_id>/judge_data", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def upload_judge_data(problem_id: int):
    if not ("judgeData" in request.files):
        raise http.BadRequest(reason="JudgeDataNotDetected")
    else:
        file = request.files["judgeData"]
        if file.filename == '':
            raise http.BadRequest(reason="EmptyJudgeData")
        else:
            problem = Problem.query.get(problem_id)
            if problem is None:
                raise http.NotFound(reason="ProblemNotFound")
            else:
                judge_scheme = judge_scheme_dict[problem.judgeScheme]

                instance = file.stream.read()
                try:
                    resolve_result = judge_scheme.resolve_judge_data(instance)
                    print(resolve_result)
                except ValidationError as e:
                    raise http.NotAcceptable(
                        reason="InvalidJudgeData",
                        detail=e.detail
                    )

                create = False
                judge_data = JudgeData.query.get(problem_id)
                if judge_data is None:
                    judge_data = JudgeData(problem=problem_id)
                    create = True

                judge_data.author = g.user.id
                judge_data.uploadTime = g.request_datetime
                judge_data.resolveResult = resolve_result
                judge_data.data = instance

                if create:
                    db.session.add(judge_data)

                db.session.commit()
                return http.Success(resolveResult=resolve_result)


# Notice: When succeed, the response body is not json
@bp.route("/problem/id/<int:problem_id>/judge_data/raw", methods=["GET"])
@require_authentication(allow_anonymous=False)
def download_judge_data(problem_id: int):
    problem = Problem.query.get(problem_id)
    if problem is None:
        raise http.NotFound(reason="ProblemNotFound")
    else:
        judge_data = JudgeData.query.get(problem_id)
        if judge_data is None:
            raise http.NotFound(reason="JudgeDataNotUploaded")
        else:
            return judge_data.data, http.OK, {"Content-Type": "application/octet-stream"}


@bp.route("/problem/id/<int:problem_id>/judge_data/resolved", methods=["GET"])
@require_authentication(allow_anonymous=False)
def retrieve_judge_data_info(problem_id: int):
    problem = Problem.query.get(problem_id)
    if problem is None:
        raise http.NotFound(reason="ProblemNotFound")
    else:
        judge_data = JudgeData.query.get(problem_id)
        if judge_data is None:
            raise http.NotFound(reason="JudgeDataNotUploaded")
        else:
            return http.Success(result=judge_data.resolveResult)
