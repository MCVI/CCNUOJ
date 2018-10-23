from enum import Enum
from sqlalchemy_utils import ChoiceType

from ..global_obj import database as db


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
    executable = 'exec'
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
