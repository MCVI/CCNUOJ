from ..global_obj import database as db

from sqlalchemy_utils import EmailType, JSONType, UUIDType


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(EmailType, nullable=False)
    shortName = db.Column(db.String(), nullable=False)

    createTime = db.Column(db.DateTime, nullable=False)
    realPersonInfo = db.Column(JSONType, nullable=False)
    extraInfo = db.Column(JSONType, nullable=True)

    uuid = db.Column(UUIDType, nullable=False)
    authentication = db.Column(JSONType, nullable=False)

    isSuper = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('email'),
        db.UniqueConstraint('shortName'),
        db.UniqueConstraint('uuid'),
    )
