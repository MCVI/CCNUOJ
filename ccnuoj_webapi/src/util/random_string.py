import random


def random_string(available_char: str, length: int) -> str:
    return ''.join(random.sample(available_char, length))
