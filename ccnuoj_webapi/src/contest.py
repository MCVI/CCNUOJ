from .util import http
from .model import Contest, User
from .global_obj import blueprint as bp


@bp.route("/contest/list", methods=["GET"])
def retrieve_contest_list():
    contest_list = Contest.query.all()

    instance = []
    for contest in contest_list:
        author: User = User.query.get(contest.author)

        inst = {
            "id": contest.id,
            "needRegister": contest.needRegister,

            "title": contest.title,
            "author": {
                "id": author.id,
                "shortName": author.shortName,
            },

            "startTime": contest.startTime,
            "endTime": contest.endTime,
        }

        instance.append(inst)

    return http.Success(result=instance)
