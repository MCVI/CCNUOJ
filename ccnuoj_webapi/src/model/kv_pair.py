from ..global_obj import database as db


class KVPair(db.Model):
    key = db.Column(db.String(), primary_key=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
