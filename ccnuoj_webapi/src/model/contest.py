from ..global_obj import database as db
from .entity import EntityMixin

from sqlalchemy_utils import ColorType


class Contest(EntityMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    freezeTime = db.Column(db.DateTime, nullable=False)
    unfreezeTime = db.Column(db.DateTime, nullable=False)

    problemList = db.relationship(
        'Problem',
        secondary='contest_problem',
        backref=db.backref('contestList', lazy='dynamic'),
        lazy='dynamic',
    )

    __table_args__ = (
        db.Index('ix_contest_author', 'author'),
    )


class ContestProblem(db.Model):
    contest = db.Column(db.Integer, db.ForeignKey('contest.id'), primary_key=True, nullable=False)
    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True, nullable=False)
    identifier = db.Column(db.String(8), nullable=False)
    color = db.Column(ColorType, nullable=False)

    __table_args__ = (
        db.Index('ix_contest_problem_contest', 'contest'),
    )
