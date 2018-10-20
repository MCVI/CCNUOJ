from abc import abstractmethod
from typing import Union


class SchemeNotFound(Exception):
    pass


class ValidationError(Exception):
    @property
    def detail(self) -> Union[None, str, dict]:
        return None


class JudgeScheme:
    @classmethod
    @abstractmethod
    def get_short_name(cls) -> str:
        pass

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
