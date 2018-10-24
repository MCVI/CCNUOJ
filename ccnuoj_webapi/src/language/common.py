from ..util.class_dict import SubClassNotFound, ElementMeta, SubClassDict


class LanguageNotFound(SubClassNotFound):
    pass


class LanguageMeta(ElementMeta):
    pass


class Language(metaclass=LanguageMeta):
    short_name = None


language_dict = SubClassDict(LanguageMeta, "short_name", LanguageNotFound)
