from enum import Enum
from sqlalchemy_utils import JSONType, ChoiceType

from ..global_obj import database as db


class JudgeState(Enum):
    waiting = 'WAIT'
    pending = 'PEND'

    compiling = 'CMPL'
    compileError = 'CE'
    compileTimeLimitExceeded = 'CTLE'

    running = 'RUN'
    runtimeError = 'RE'
    timeLimitExceeded = 'TLE'
    memoryLimitExceeded = 'MLE'
    outputLimitExceeded = 'OLE'

    comparing = 'CMPR'

    accepted = 'AC'
    wrongAnswer = 'WA'
    presentationError = 'PE'

    systemError = 'SYSE'


JudgeStateType = ChoiceType(JudgeState, impl=db.String(4))


class JudgeData(db.Model):
    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploadTime = db.Column(db.DateTime, nullable=False)

    resolveResult = db.Column(JSONType, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)


class JudgeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    submission = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)

    operator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reason = db.Column(db.Text, nullable=True)

    createTime = db.Column(db.DateTime, nullable=False)
    finishTime = db.Column(db.DateTime, nullable=True)

    state = db.Column(JudgeStateType, nullable=False)

    __table_args__ = (
        db.Index('ix_judge_request_submission', 'submission'),
        db.Index('ix_judge_request_operator', 'operator'),
    )


class JudgeCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    operator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    judgeRequest = db.Column(db.Integer, db.ForeignKey('judge_request.id'), nullable=True)

    createTime = db.Column(db.DateTime, nullable=False)
    command = db.Column(JSONType, nullable=False)

    fetchTime = db.Column(db.DateTime, nullable=True)

    finishTime = db.Column(db.DateTime, nullable=True)
    result = db.Column(JSONType, nullable=True)

    __table_args__ = (
        db.Index('ix_judge_command_operator', 'operator'),
        db.UniqueConstraint('judgeRequest'),
    )
