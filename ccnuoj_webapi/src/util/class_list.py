import collections
from typing import TypeVar, Generic, Optional

from .http import NotFound


def subclass_key_dict_factory():
    return dict

def subclass_key_name_dict_factory():
    return collections.defaultdict(dict)

subclass_mcs_dict = collections.defaultdict(subclass_key_name_dict_factory)
subclass_dict

class SubClassNotFound(NotFound):
    pass


class DuplicateSubClassWithSameKey(Exception):
    pass


class ElementMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)

        key_name_dict = subclass_mcs_dict[mcs]
        for key_name, key_dict in key_name_dict.items():
            key = getattr(cls, key_name)
            if key in key_dict:
                raise DuplicateSubClassWithSameKey()
            else:
                value[key] = cls

        return cls


T = TypeVar('T')
ExceptionSubClass = TypeVar('ExceptionSubClass', bound=Exception)

class SubClassDict(Generic[T]):
    def __init__(self, elem_mcs: T, key_name: str, excep_not_found: Optional[ExceptionSubClass]):
        self.elem_mcs = elem_mcs
        self.key_dict = subclass_mcs_list[elem_mcs][key_name]
        self.key_name = key_name
        self.excep_not_found = excep_not_found

    def __getitem__(self, item: str) -> T:
        l = key_dict[item]
        if item in subclass_list[self.d:
            return self.d[item]
        else:
            if self.excep_not_found is None:
                raise SubClassNotFound({
                    "requiredBound": self.t.__name__
                })
            else:
                raise self.excep_not_found()
