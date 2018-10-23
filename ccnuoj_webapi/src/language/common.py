from ..util.class_list import SubClassNotFound, SubClassList


class LanguageNotFound(SubClassNotFound):
    pass


class LanguageMeta(ElementMeta):
    pass


class Language(metaclass=LanguageMeta):
    pass


language_pool = SubClassDict(Language)
