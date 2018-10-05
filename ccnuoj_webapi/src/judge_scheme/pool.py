from typing import TypeVar

from .common import SchemeNotFound, JudgeScheme


scheme_pool = {}


class JudgeSchemeShortNameConflict(Exception):
    pass


def get(short_name: str) -> JudgeScheme:
    if short_name in scheme_pool:
        return scheme_pool[short_name]
    else:
        raise SchemeNotFound()


CLS = TypeVar('CLS', bound=JudgeScheme)


def add_to_pool(cls: CLS) -> CLS:
    short_name = cls.get_short_name()

    if short_name in scheme_pool:
        raise JudgeSchemeShortNameConflict()
    else:
        scheme_pool[short_name] = cls
        return cls
