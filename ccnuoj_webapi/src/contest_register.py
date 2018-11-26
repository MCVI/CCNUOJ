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
