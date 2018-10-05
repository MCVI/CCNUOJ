import jsonschema

from . import common
from .pool import add_to_pool


@add_to_pool
class SimpleComparison(common.JudgeScheme):
    @classmethod
    def get_short_name(cls) -> str:
        return "SimpComp"

    @classmethod
    def validate_limit_info(cls, limit_info: dict) -> None:
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties":{
                "time": {
                    "description": "time limit in milliseconds",
                    "type": "number"
                },
                "memory": {
                    "description": "memory limit in megabytes",
                    "type": "number"
                }
            },
            "required": ["time", "memory"],
            "additionalProperties": False
        }
        try:
            jsonschema.validate(instance=limit_info, schema=schema)
        except jsonschema.ValidationError:
            raise common.ValidationError()

    @classmethod
    def validate_judge_param(cls, judge_param: dict) -> None:
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "properties": {},
            "additionalProperties": False
        }
        try:
            jsonschema.validate(instance=judge_param, schema=schema)
        except jsonschema.ValidationError:
            raise common.ValidationError()
