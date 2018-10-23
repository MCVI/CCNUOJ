from sqlalchemy_utils import JSONType

from ..global_obj import database as db

from .types import JudgeSchemeType
from .entity import EntityMixin


class Problem(EntityMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    judgeScheme = db.Column(JudgeSchemeType, nullable=False)
    limitInfo = db.Column(JSONType, nullable=False)

    __table_args__ = (
        db.Index('ix_problem_author', 'author'),
    )
