import jsonschema

from .common import JudgeScheme, ValidationError


class SimpleComparison(JudgeScheme):
    short_name = "SimpComp"
    supported_language = ["cpp"]

    @classmethod
    def validate_limit_info(cls, limit_info: dict) -> None:
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
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
            raise ValidationError()

    @classmethod
    def resolve_judge_data(cls, judge_data: bytes) -> dict:
        """ !! stub """
        return {}
