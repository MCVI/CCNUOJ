from ..global_obj import database as db

from .types import LanguageType


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    createTime = db.Column(db.DateTime, nullable=False)

    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    contest = db.Column(db.Integer, db.ForeignKey('contest.id'), nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    language = db.Column(LanguageType, nullable=False)
    text = db.Column(db.Text, nullable=False)

    judgeRequests = db.relationship(
        'JudgeRequest',
        lazy='dynamic',
    )

    __table_args__ = (
        db.Index('ix_submission_problem', 'problem'),
        db.Index('ix_submission_contest', 'contest'),
        db.Index('ix_submission_author', 'author'),
    )
