from flask import g

from .util import http, get_request_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import Contest, User, ContestRegister, contest_register_info_schema
from .authentication import require_authentication


@bp.route("/contest/id/<int:contest_id>/register/user/id/<int:user_id>", methods=["POST"])
@require_authentication(allow_anonymous=False)
def create_register(contest_id: int, user_id:int):
    instance = get_request_json(schema=contest_register_info_schema)

    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    user: User = None
    if (user_id == g.user.id) or g.user.isSuper:
        user = User.query.get(user_id)
    else:
        raise http.Forbidden(reason="PermissionDenied")

    register: ContestRegister = ContestRegister.query.get((contest.id, user.id))

    if register is None:
        register = ContestRegister()
        register.contest = contest.id
        register.user = user.id
        register.registerTime = g.request_datetime
        register.passed = False
        register.registerInfo = instance

        db.session.add(register)
        db.session.commit()

        return http.Success(registerTime=register.registerTime)

    else:
        raise http.Conflict(
            reason="RegisterAlreadyExisted",
            detail={
                "registerTime": register.registerTime,
            }
        )


@bp.route("/contest/id/<int:contest_id>/register/user/id/<int:user_id>", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def update_register(contest_id: int, user_id: int):
    instance = get_request_json(schema=contest_register_info_schema)

    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    user: User = None
    if (user_id == g.user.id) or g.user.isSuper:
        user = User.query.get(user_id)
    else:
        raise http.Forbidden(reason="PermissionDenied")

    register: ContestRegister = ContestRegister.query.get((contest.id, user.id))

    if register is None:
        raise http.NotFound(reason="RegisterNotFound")
    else:
        if g.user.isSuper or not register.passed:
            register.registerInfo = instance
            register.registerTime = g.request_datetime

            db.session.commit()
            return http.Success(registerTime=register.registerTime)

        else:
            raise http.Conflict(reason="RegisterAlreadyPassed")


@bp.route("/contest/id/<int:contest_id>/register/user/id/<int:user_id>", methods=["GET"])
@require_authentication(allow_anonymous=False)
def retrieve_register(contest_id: int, user_id: int):
    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    user: User = None
    if (user_id == g.user.id) or g.user.isSuper:
        user = User.query.get(user_id)
    else:
        raise http.Forbidden(reason="PermissionDenied")

    register: ContestRegister = ContestRegister.query.get((contest.id, user.id))
    if register is None:
        raise http.NotFound(reason="RegisterNotFound")
    else:
        return http.Success(result={
            "registerInfo": register.registerInfo,
            "registerTime": register.registerTime,
            "passed": register.passed,
        })


@bp.route("/contest/id/<int:contest_id>/register/user/id/<int:user_id>", methods=["DELETE"])
@require_authentication(allow_anonymous=False)
def delete_register(contest_id: int, user_id: int):
    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    user: User = None
    if (user_id == g.user.id) or g.user.isSuper:
        user = User.query.get(user_id)
    else:
        raise http.Forbidden(reason="PermissionDenied")

    register: ContestRegister = ContestRegister.query.get((contest.id, user.id))
    if register is None:
        raise http.NotFound(reason="RegisterNotFound")
    else:
        if g.user.isSuper or not register.passed:
            db.session.delete(register)

            db.session.commit()
            return http.Success()

        else:
            raise http.Conflict(reason="RegisterAlreadyPassed")


@bp.route("/contest/id/<int:contest_id>/register/user/id/<int:user_id>/passed", methods=["PUT"])
@require_authentication(allow_anonymous=False)
def update_register_passed(contest_id: int, user_id: int):
    instance = get_request_json(schema={
        "type": "object",
        "properties": {
            "passed": {
                "type": "boolean",
            },
        },
        "required": ["passed"],
        "additionalProperties": False,
    })

    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    if not ((g.user.id == contest.author) or g.user.isSuper):
        raise http.Forbidden(reason="PermissionDenied")

    user: User = User.query.get(user_id)
    if user is None:
        raise http.NotFound(reason="UserNotFound")

    register: ContestRegister = ContestRegister.query.get((contest.id, user.id))

    if register is None:
        raise http.NotFound(reason="RegisterNotFound")
    else:
        register.passed = instance["passed"]

        db.session.commit()
        return http.Success()


@bp.route("/contest/id/<int:contest_id>/register/filter/all/page/<int:page_num>", methods=["GET"])
@require_authentication(allow_anonymous=False)
def get_register_list(contest_id: int, page_num: int):
    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    if not ((g.user.id == contest.author) or g.user.isSuper):
        raise http.Forbidden(reason="PermissionDenied")

    pagination = ContestRegister.query.filter_by(
        contest=contest.id
    ).paginate(
        page=page_num,
        error_out=False
    )
    page_count = pagination.pages
    register_list = pagination.items

    passed_count = 0
    instance = []
    for register in register_list:
        inst = {
            "userID": register.user,
            "registerInfo": register.registerInfo,
            "registerTime": register.registerTime,
            "passed": register.passed,
        }
        instance.append(inst)

        if register.passed:
            passed_count = passed_count + 1

    return http.Success(result={
        "totalNum": len(instance),
        "passedNum": passed_count,

        "pageCount": page_count,
        "list": instance,
    })


@bp.route("/contest/id/<int:contest_id>/register/filter/passed/page/<int:page_num>", methods=["GET"])
def get_register_passed_list(contest_id: int, page_num: int):
    contest = Contest.query.get(contest_id)
    if contest is None:
        raise http.NotFound(reason="ContestNotFound")
    elif not contest.needRegister:
        raise http.Conflict(reason="NoRegisterInContest")

    pagination = ContestRegister.query.filter_by(
        contest=contest.id,
        passed=True
    ).paginate(
        page=page_num,
        error_out=False
    )
    page_count = pagination.pages
    register_list = pagination.items

    instance = []
    for register in register_list:
        inst = {
            "registerInfo": {
                "realName": register.registerInfo["realName"],
                "studentInfo": {
                    "school": register.registerInfo["studentInfo"]["school"],
                },
            },
            "passed": register.passed,
        }
        instance.append(inst)

    return http.Success(result={
        "passedNum": len(instance),

        "pageCount": page_count,
        "list": instance,
    })
