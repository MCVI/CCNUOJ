import jsonschema
from flask import request, json


def get_request_json(schema: dict, force=True, silent=False, cache=True):
    instance = request.get_json(force=force, silent=silent, cache=cache)
    jsonschema.validate(instance=instance, schema=schema)
    return instance


def to_json(obj: dict):
    return json.dumps(obj)
