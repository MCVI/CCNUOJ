from abc import abstractmethod
from typing import Union

from ..util.class_dict import ElementMeta, SubClassDict, SubClassNotFound


class JudgeSchemeNotFound(SubClassNotFound):
    pass


class ValidationError(Exception):
    @property
    def detail(self) -> Union[None, str, dict]:
        return None


class JudgeSchemeMeta(ElementMeta):
    pass


class JudgeScheme(metaclass=JudgeSchemeMeta):
    short_name = None

    @classmethod
    @abstractmethod
    def validate_limit_info(cls, limit_info: dict) -> None:
        """
        raise ValidationError if limit_info is invalid
        :return: None
        """
        pass

    @classmethod
    @abstractmethod
    def resolve_judge_data(cls, judge_data: bytes) -> dict:
        """
        raise ValidationError if judge_data is invalid
        :return: resolveResult
        """
        pass


judge_scheme_dict = SubClassDict(JudgeSchemeMeta, "short_name", JudgeSchemeNotFound)
