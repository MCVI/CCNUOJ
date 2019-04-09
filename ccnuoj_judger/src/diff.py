import re


ignore_all_space = re.compile(r'\s+')
ignore_trailing = re.compile(r'(\n+$)|( +(?=\n))')


def diff_ignore_all_space(a: str, b: str) -> bool:
    sa = ignore_all_space.sub('', a)
    sb = ignore_all_space.sub('', b)
    return sa == sb


def diff_ignore_trailing(a: str, b: str) -> bool:
    sa = ignore_trailing.sub('', a)
    sb = ignore_trailing.sub('', b)
    return sa == sb
