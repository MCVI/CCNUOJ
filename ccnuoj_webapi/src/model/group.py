from sqlalchemy_utils import JSONType

from ..global_obj import database as db


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


class UserGroup(db.Model):
    user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True, nullable=False)

    __table_args__ = (
        db.Index('ix_user_group_user', 'user'),
        db.Index('ix_user_group_group', 'group'),
    )
