from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import JSONType

from ..global_obj import database as db


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
