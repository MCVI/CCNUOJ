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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nickname = db.Column(db.String(), unique=True, index=True, nullable=False)
    email = db.Column(EmailType, unique=True, index=True, nullable=False)

    createTime = db.Column(db.DateTime, nullable=False)
    realPersonInfo = db.Column(JSONType, nullable=False)
    extraInfo = db.Column(JSONType, nullable=True)

    auth = db.Column(JSONType, nullable=False)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    displayName = db.Column(db.String(), unique=True, nullable=False)
    extraInfo = db.Column(JSONType, nullable=False)

    userList = db.relationship(
        'User',
        secondary=UserGroup,
        backref=db.backref('groupList', lazy='dynamic'),
        lazy='dynamic',
    )


class AccessControlObjectType(Enum):
    User = 'user'
    Group = 'group'


class AccessLevel(Enum):
    readable = 'readable'
    editable = 'editable'
    fullControl = 'fullControl'


class AccessControlList(db.Model):
    group = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True, nullable=False)
    objType = db.Column(ChoiceType(AccessControlObjectType), primary_key=True, nullable=False)
    objId = db.Column(db.Integer, primary_key=True, nullable=False)
    level = db.Column(ChoiceType(AccessLevel), nullable=False)


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

    judgeScheme = db.Column(db.Integer, db.ForeignKey('judge_scheme.id'), primary_key=True, nullable=False)
    judgeParam = db.Column(JSONType, nullable=False)


class JudgeScheme(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    displayName = db.Column(db.String(), nullable=False)
    extraInfo = db.Column(JSONType, nullable=False)

    script = db.Column(db.Text, nullable=False)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    contest = db.Column(db.Integer, db.ForeignKey('contest.id'), nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    text = db.Column(db.Text, nullable=False)

    judgeScheme = db.Column(db.Integer, db.ForeignKey('judge_scheme.id'), nullable=False)
    judgeParam = db.Column(JSONType, nullable=False)


class ContestProblem(db.Model):
    contest = db.Column(db.Integer, db.ForeignKey('contest.id'), primary_key=True, nullable=False)
    problem = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True, nullable=False)
    identifier = db.Column(db.String(8), nullable=False)
    color = db.Column(ColorType, nullable=False)


class Contest(EntityMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    freezeTime = db.Column(db.DateTime, nullable=False)
    unfreezeTime = db.Column(db.DateTime, nullable=False)

    problemList = db.relationship(
        'Problem',
        secondary=ContestProblem,
        backref=db.backref('contestList', lazy='dynamic'),
        lazy='dynamic',
    )
