import string
import hashlib
from functools import wraps
from flask import Flask, request, g
from flask import current_app as app
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import BadSignature, SignatureExpired

from .util import random_string
from .util import get_request_json, to_json
from .util import HTTPStatusCode
from .global_obj import blueprint as bp
from .model import User


salt_available_char = string.ascii_letters+string.digits


def init(app: Flask):
    secret_key = app.config['CCNU_AUTH_TOKEN_SECRET_KEY']
    expiration = app.config['CCNU_AUTH_TOKEN_EXPIRATION']
    global signer
    signer = TimedJSONWebSignatureSerializer(
        secret_key=secret_key,
        expires_in=expiration,
        algorithm_name='HS512'
    )


def server_hash(salt, text) -> str:
    full_text = '-'.join([
        salt["front"],
        app.config['CCNU_SERVER_FIXED_SALT'],
        text,
        salt["back"]
    ])
    hash_obj = hashlib.sha512()
    hash_obj.update(full_text.encode('UTF-8'))
    return hash_obj.hexdigest()


def sign_auth_token(user: User) -> str:
    payload = {
        "id": user.id,
        "uuid": user.uuid.hex,
        "random": random_string(salt_available_char, 8)
    }
    return signer.dumps(payload).decode('ASCII')


@bp.route('/user/authentication_info/email/<string:email>', methods=["GET"])
def get_info_by_email(email: str):
    user = User.query.filter_by(email=email).first()
    return get_info(user)


@bp.route('/user/authentication_info/shortName/<string:username>', methods=["GET"])
def get_info_by_username(username: str):
    user = User.query.filter_by(shortName=username).first()
    return get_info(user)


def get_info(user: User):
    return to_json({
        "id": user.id,
        "salt": user.authentication["clientSalt"]
    })


@bp.route('/user/authentication/id/<int:user_id>', methods=["POST"])
def auth_by_id(user_id: int):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "user authentication",
        "type": "object",
        "properties": {
            "hashResult": {
                "type": "string"
            }
        },
        "required": ["hashResult"]
    }
    instance = get_request_json(schema=schema)

    user = User.query.get(user_id)
    server_hash_result = server_hash(user.authentication["serverSalt"], instance["hashResult"])
    if user.authentication["hashResult"] == server_hash_result:
        token = sign_auth_token(user)
        return to_json({
            "status": "success",
            "token": token
        })
    else:
        return to_json({
            "status": "failed",
            "reason": "password_mismatch"
        }), HTTPStatusCode.Unauthorized


class NoTokenDetected(BaseException):
    pass


class InvalidToken(BaseException):
    pass


class TokenExpired(BaseException):
    pass


def load_token():
    if 'X-CCNU-AUTH-TOKEN' in request.headers.has_key:

        token = request.headers['X-CCNU-AUTH-TOKEN']

        try:
            payload = signer.loads(token)
        except BadSignature:
            raise InvalidToken()
        except SignatureExpired:
            raise TokenExpired()

        user = User.query.get(payload["id"])
        if user.uuid == payload["uuid"]:
            return user
        else:
            raise InvalidToken()

    else:
        raise NoTokenDetected()


def require_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            token_load_failed = False

            try:
                user = load_token()
            except:
                token_load_failed = True
                raise

        except NoTokenDetected:
            pass
        except InvalidToken:
            pass
        except TokenExpired:
            pass

        if token_load_failed:
            return to_json({
                "status": "failed",
                "reason": "require_authentication"
            }), HTTPStatusCode.Unauthorized
        else:
            g.user = user
            func(*args, **kwargs)

    return wrapper
