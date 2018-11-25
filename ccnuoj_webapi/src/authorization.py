from functools import wraps
from flask import g

from .util import http
from .authentication import require_authentication


def require_super(func):

    @wraps(func)
    @require_authentication(allow_anonymous=False)
    def wrapper(*args, **kwargs):
        if g.user.isSuper:
            return func(*args, **kwargs)
        else:
            return http.Forbidden(reason="PermissionDenied")

    return wrapper
