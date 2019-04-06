from ..global_obj import database as db


class KVPair(db.Model):
    key = db.Column(db.String(), primary_key=True, nullable=False)
    value = db.Column(db.Text, nullable=True)


def get_kv(key: str) -> str:
    pair = KVPair.query.get(key)
    return pair.value


def set_kv(key: str, value: str) -> None:
    pair = KVPair()
    pair.key = key
    pair.value = value
    db.session.add(pair)
