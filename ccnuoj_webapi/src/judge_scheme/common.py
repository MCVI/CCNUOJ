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
    def validate_judge_param(cls, judge_param: dict) -> None:
        """
        raise ValidationError if judge_param is invalid
        :return: None
        """
        pass
