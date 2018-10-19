from flask import request, g

from .util import http, to_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Problem, JudgeScheme, JudgeData
from .authentication import require_authentication
from . import judge_scheme


# Notice: The request body is not supposed to be json
@bp.route("/problem/id/<int:id>/judge_data", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def upload_judge_data(problem_id: int):
    if not ("judgeData" in request.files):
        raise http.BadRequest(body={
            "status": "Failed",
            "reason": "JudgeDataNotDetected"
        })
    else:
        file = request.files["judgeData"]
        if file.filename == '':
            raise http.BadRequest(body={
                "status": "Failed",
                "reason": "EmptyJudgeData"
            })
        else:
            problem = Problem.query.get(problem_id)
            if problem is None:
                raise http.NotFound(body={
                    "status": "Failed",
                    "reason": "ProblemNotFound"
                })
            else:
                judge_scheme_rec = JudgeScheme.query.get(problem.judgeScheme)
                judge_scheme_cls = judge_scheme.get(judge_scheme_rec.shortName)

                instance = file.stream.read()
                try:
                    resolve_result = judge_scheme_cls.resolve_judge_data(instance)
                except judge_scheme.ValidationError as e:
                    raise http.NotAcceptable(body={
                        "status": "Failed",
                        "reason": "InvalidJudgeData",
                        "detail": e.detail
                    })

                create = False
                judge_data = JudgeData.query.get(problem_id)
                if judge_data is None:
                    judge_data = JudgeData(problem=problem_id)
                    create = True

                judge_data.author = g.user.id
                judge_data.uploadTime = g.request_datetime
                judge_data.data = instance

                if create:
                    db.session.add(judge_data)

                db.session.commit()
                return to_json({
                    "status": "Success",
                    "resolveResult": resolve_result
                })
