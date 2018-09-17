import uuid
from flask import g

from .util import random_string, get_request_json, to_json
from .global_obj import database as db
from .global_obj import blueprint as bp
from .model import User
from .authentication import salt_available_char, server_hash


@bp.route('/user', methods=["POST"])
def create_user():
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "create a new user",
        "type": "object",
        "properties": {
            "email": {
                "description": "account email for login",
                "type": "string",
                "format": "email"
            },
            "shortName": {
                "description": "short user name for login",
                "type": "string"
            },
            "realPersonInfo": {
                "description": "information about identity in reality",
                "type": "object"
            },
            "extraInfo": {
                "description": "extra information to store",
                "type": "object"
            },
            "authentication": {
                "description": "authentication information",
                "type": "object",
                "properties": {
                    "salt": {
                        "description": "random salt generated at client",
                        "type": "object",
                        "properties": {
                            "front": {
                                "type": "string"
                            },
                            "back": {
                                "type": "string"
                            }
                        },
                        "required": ["front", "back"]
                    },
                    "hashResult": {
                        "type": "string"
                    }
                },
                "required": ["salt", "hashResult"]
            }
        },
        "required": ["email", "shortName", "realPersonInfo", "extraInfo", "authentication"]
    }
    instance = get_request_json(schema=schema)

    user = User()
    for key in ["email", "shortName", "realPersonInfo", "extraInfo"]:
        value = instance[key]
        setattr(user, key, value)

    server_random_salt = {
        "front": random_string(salt_available_char, 8),
        "back": random_string(salt_available_char, 8)
    }
    server_hash_result = server_hash(server_random_salt, instance["authentication"]["hashResult"])
    user.authentication = {
        "clientSalt": instance["authentication"]["salt"],
        "serverSalt": server_random_salt,
        "hashResult": server_hash_result
    }

    user.createTime = g.request_datetime
    user.uuid = uuid.uuid1()
    db.session.add(user)
    db.session.commit()

    return to_json({
        "status": "success"
    })
