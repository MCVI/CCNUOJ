import collections
from typing import TypeVar, Generic
from typing import Dict, List, Union


def subclass_key_name_dict_factory() -> Dict[Union[None, str], Union[List, Dict]]:
    return {
        None: []
    }


subclass_mcs_dict = collections.defaultdict(subclass_key_name_dict_factory)


class SubClassNotFound(KeyError):
    pass


class ElementMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)

        key_name_dict = subclass_mcs_dict[mcs]
        for (key_name, key_dict) in key_name_dict.items():
            if key_name is None:
                key_dict.append(cls)
            else:
                key = getattr(cls, key_name)
                assert(key not in key_dict)
                key_dict[key] = cls

        return cls


T = TypeVar('T')


class SubClassDict(Generic[T]):
    def __init__(self, elem_mcs: T, key_name: str, excep_not_found=SubClassNotFound):
        self.elem_mcs = elem_mcs

        key_name_dict = subclass_mcs_dict[elem_mcs]
        if key_name not in key_name_dict:
            key_name_dict[key_name] = {}
            key_dict = key_name_dict[key_name]
            for cls in key_name_dict[None]:
                key = getattr(cls, key_name)
                key_dict[key] = cls
        self.key_dict = subclass_mcs_dict[elem_mcs][key_name]
        self.key_name = key_name
        self.excep_not_found = excep_not_found

    def __getitem__(self, item: str) -> T:
        if item in self.key_dict:
            return self.key_dict[item]
        else:
            raise self.excep_not_found()
