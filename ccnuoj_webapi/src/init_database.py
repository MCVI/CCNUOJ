import string

from .util import random_string
from .global_obj import database as db
from .model import set_kv


def init_database():
    db.create_all()

    available_char = string.ascii_letters+string.digits

    auth_token_secret_key = random_string(available_char, 14)
    set_kv('AuthTokenSecretKey', auth_token_secret_key)

    auth_server_fixed_salt = random_string(available_char, 14)
    set_kv('AuthServerFixedSalt', auth_server_fixed_salt)

    auth_client_fixed_salt = random_string(available_char, 14)
    set_kv('AuthClientFixedSalt', auth_client_fixed_salt)

    db.session.commit()

    print('Successfully Initialized Database')
