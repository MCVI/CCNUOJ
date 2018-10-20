import werkzeug.exceptions
from flask import json


OK = 200


class HTTPException(werkzeug.exceptions.HTTPException):
    code = None

    def __init__(self, body={}):
        super().__init__()
        self.body = body
        self.description = json.dumps(body)

    @property
    def name(self):
        if "reason" in self.body:
            return self.body["name"]
        else:
            return "UnknownError"

    def get_body(self, environ=None):
        return self.description

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class BadRequest(HTTPException):
    code = 400


class Unauthorized(HTTPException):
    code =401


class NotFound(HTTPException):
    code = 404


class InternalServerError(HTTPException):
    code = 500


class NotAcceptable(HTTPException):
    code = 406


class Conflict(HTTPException):
    code = 409


class Gone(HTTPException):
    code = 410


class NotImplemented(HTTPException):
    code = 501
