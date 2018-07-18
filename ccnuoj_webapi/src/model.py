from enum import Enum
from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, JSONType, ChoiceType, ColorType

db = SQLAlchemy()


class KVPair(db.Model):
    key = db.Column(db.String(), primary_key=True, nullable=False)
    value = db.Column(db.Text, nullable=True)


class UserGroup(db.Model):
    user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True, nullable=False)

    __table_args__ = (
        db.Index('ix_user_group_user', 'user'),
        db.Index('ix_user_group_group', 'group'),
    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(EmailType, nullable=False)
    shortName = db.Column(db.String(), nullable=False)

    createTime = db.Column(db.DateTime, nullable=False)
    realPersonInfo = db.Column(JSONType, nullable=False)
    extraInfo = db.Column(JSONType, nullable=True)

    auth = db.Column(JSONType, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('email'),
        db.UniqueConstraint('shortName'),
    )


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    displayName = db.Column(db.String(), nullable=False)
    extraInfo = db.Column(JSONType, nullable=False)

    userList = db.relationship(
        'User',
        secondary='user_group',
        backref=db.backref('groupList', lazy='dynamic'),
        lazy='dynamic',
    )

    __table_args__ = (
        db.UniqueConstraint('displayName'),
    )


class AccessControlSubjectEnum(Enum):
    User = 'USER'
    Group = 'GRP'


class AccessControlObjectEnum(Enum):
    Super = 'SUPR'
    ServerOperation = 'SERV'

    User = 'USER'
    Problem = 'PRBL'
    Contest = 'CNTS'


AccessControlSubjectEnumType = ChoiceType(AccessControlSubjectEnum, impl=db.String(4))
AccessControlObjectEnumType = ChoiceType(AccessControlObjectEnum, impl=db.String(4))


class AccessLevel(Enum):
    readable = 'read'
    editable = 'edit'
    fullControl = 'full'


AccessLevelType = ChoiceType(AccessLevel, impl=db.String(4))


class AccessControlList(db.Model):
    subjectType = db.Column(AccessControlSubjectEnumType, primary_key=True, nullable=False)
    subjectId = db.Column(db.Integer, primary_key=True, nullable=True)
    objectType = db.Column(AccessControlObjectEnumType, primary_key=True, nullable=False)
    objectId = db.Column(db.Integer, primary_key=True, nullable=True)
    level = db.Column(AccessLevelType, nullable=False)

    __table_args__ = (
        db.Index('ix_access_control_list_subjectType_subjectId', 'subjectType', 'subjectId'),
        db.Index('ix_access_control_list_objectType_objectId', 'objectType', 'objectId'),
    )


class TimestampMixin:
    createTime = db.Column(db.DateTime, nullable=False)
    lastModifiedTime = db.Column(db.DateTime, nullable=False)


class EntityMixin(TimestampMixin):
    @declared_attr
    def author(self):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.Text, nullable=False)
    extraInfo = db.Column(JSONType, nullable=False)


class Problem(EntityMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    timeLimit = db.Column(db.Integer, nullable=False)
    memoryLimit = db.Column(db.Integer, nullable=False)
    judgeScheme = db.Column(db.Integer, db.ForeignKey('judge_scheme.id'), nullable=False)
    judgeParam = db.Column(JSONType, nullable=False)

    __table_args__ = (
        db.Index('ix_problem_author', 'author'),
    )

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    shortName = db.Column(db.String(8), nullable=False)
    displayName = db.Column(db.String(), nullable=False)

    script = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('shortName'),
        db.UniqueConstraint('displayName'),
    )

class JudgeSchemeLanguage(db.Model):
    judgeScheme = db.Column(db.Integer, db.ForeignKey('judge_scheme.id'), primary_key=True, nullable=False)
    language = db.Column(db.String(8), db.ForeignKey('language.id'), primary_key=True, nullable=False)

    __table_args__ = (
        db.Index('ix_judge_scheme_language_judge_scheme', 'judgeScheme'),
    )


class JudgeScheme(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    displayName = db.Column(db.String(), nullable=False)
    extraInfo = db.Column(JSONType, nullable=False)

    script = db.Column(db.Text, nullable=False)

    languages = db.relationship(
        'Language',
        secondary='judge_scheme_language',
        lazy='dynamic',
    )

    __table_args__ = (
        db.UniqueConstraint('displayName'),
    )


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    createTime = db.Column(db.DateTime, nullable=False)

    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    contest = db.Column(db.Integer, db.ForeignKey('contest.id'), nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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


class JudgeState(Enum):
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


class JudgeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    submission = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)

    operator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reason = db.Column(db.Text, nullable=True)

    createTime = db.Column(db.DateTime, nullable=False)
    finishTime = db.Column(db.DateTime, nullable=True)

    state = db.Column(JudgeStateType, nullable=False)

    judgeCommand = db.Column(db.Integer, db.ForeignKey('judge_command.id'), nullable=False)

    __table_args__ = (
        db.Index('ix_judge_request_submission', 'submission'),
        db.Index('ix_judge_request_operator', 'operator'),
        db.UniqueConstraint('judgeCommand'),
    )


class JudgeCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    operator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    createTime = db.Column(db.DateTime, nullable=False)
    command = db.Column(JSONType, nullable=False)

    finishTime = db.Column(db.DateTime, nullable=True)
    result = db.Column(JSONType, nullable=True)

    __table_args__ = (
        db.Index('ix_judge_command_operator', 'operator'),
    )


class ContestProblem(db.Model):
    contest = db.Column(db.Integer, db.ForeignKey('contest.id'), primary_key=True, nullable=False)
    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True, nullable=False)
    identifier = db.Column(db.String(8), nullable=False)
    color = db.Column(ColorType, nullable=False)

    __table_args__ = (
        db.Index('ix_contest_problem_contest', 'contest'),
    )


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
