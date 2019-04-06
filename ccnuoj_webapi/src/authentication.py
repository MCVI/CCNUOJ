import uuid
import string
import hashlib
from functools import wraps
from flask import Flask, request, g, current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import BadSignature, SignatureExpired

from .util import random_string
from .util import get_request_json
from .util import http
from .global_obj import blueprint as bp
from .model import User, get_kv


module_inited = False

salt_available_char = string.ascii_letters+string.digits


def do_init(app: Flask):
    secret_key = get_kv('AuthTokenSecretKey')
    expiration = app.config['CCNU_AUTH_TOKEN_EXPIRATION']
    global signer
    signer = TimedJSONWebSignatureSerializer(
        secret_key=secret_key,
        expires_in=expiration,
        algorithm_name='HS512'
    )
    global server_fixed_salt
    server_fixed_salt = get_kv('AuthServerFixedSalt')
    global client_fixed_salt
    client_fixed_salt = get_kv('AuthClientFixedSalt')


def need_init(wrapped: callable) -> callable:

    @wraps(wrapped)
    def func(*args, **kwargs):
        global module_inited
        if not module_inited:
            do_init(current_app)
            module_inited = True

        return wrapped(*args, **kwargs)

    return func


@need_init
def server_hash(salt, text) -> str:
    full_text = '-'.join([
        salt["front"],
        server_fixed_salt,
        text,
        salt["back"]
    ])
    hash_obj = hashlib.sha512()
    hash_obj.update(full_text.encode('UTF-8'))
    return hash_obj.hexdigest()


@need_init
def sign_auth_token(user: User) -> str:
    payload = {
        "id": user.id,
        "uuid": user.uuid.hex,
        "random": random_string(salt_available_char, 8)
    }
    return signer.dumps(payload).decode('ASCII')


def get_auth_info(user: User):
    return {
        "id": user.id,
        "salt": user.authentication["clientSalt"],
    }


@bp.route("/user/authentication_info/fixed_salt", methods=["GET"])
@need_init
def get_client_fixed_salt():
    return http.Success(result={
        "fixed": client_fixed_salt,
    })


@bp.route("/user/authentication_info/email/<string:email>", methods=["GET"])
def get_info_by_email(email: str):
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise http.NotFound()
    else:
        return http.Success(result=get_auth_info(user))


@bp.route("/user/authentication_info/shortName/<string:username>", methods=["GET"])
def get_info_by_username(username: str):
    user = User.query.filter_by(shortName=username).first()
    if user is None:
        raise http.NotFound()
    else:
        return http.Success(result=get_auth_info(user))


@bp.route("/user/authentication/id/<int:user_id>", methods=["POST"])
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
        g.user_auth_token = sign_auth_token(user)
        g.user = user
        return get_auth_echo()
    else:
        raise http.Conflict(reason="PasswordMismatch")


class NoTokenDetected(Exception):
    pass


class InvalidToken(Exception):
    pass


class TokenExpired(Exception):
    pass


def load_token():
    if 'X-CCNU-AUTH-TOKEN' in request.headers:

        token = request.headers['X-CCNU-AUTH-TOKEN']

        try:
            payload = signer.loads(token)
        except BadSignature:
            raise InvalidToken()
        except SignatureExpired:
            raise TokenExpired()

        user = User.query.get(payload["id"])
        if (user is not None) and (user.uuid == uuid.UUID(payload["uuid"])):
            return user, token
        else:
            raise InvalidToken()

    else:
        raise NoTokenDetected()


def require_authentication(allow_anonymous: bool=False):

    def decorator(func: callable):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not hasattr(g, "user"):

                try:
                    user, token = load_token()
                    token_status = "Valid"
                except NoTokenDetected:
                    token_status = "NotDetected"
                except InvalidToken:
                    token_status = "Invalid"
                except TokenExpired:
                    token_status = "Expired"

                if token_status == "Valid":
                    current_user = user
                    current_token = token
                else:
                    if allow_anonymous:
                        current_user = None
                        current_token = None
                    else:
                        raise http.Unauthorized(
                            reason="AuthenticationFailed",
                            detail={
                                "tokenStatus": token_status
                            }
                        )
                g.user = current_user
                g.user_auth_token = current_token

            return func(*args, **kwargs)

        return wrapper

    return decorator


@bp.route("/user/authentication/echo", methods=["GET"])
@require_authentication(allow_anonymous=False)
def get_auth_echo():
    return http.Success(result={
        "id": g.user.id,
        "email": g.user.email,
        "shortName": g.user.shortName,
        "token": g.user_auth_token,
        "isSuper": g.user.isSuper,
    })
