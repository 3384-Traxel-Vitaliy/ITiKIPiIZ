import re
from functools import lru_cache


@lru_cache(maxsize=200000)
def norm(word):
    return word.lower().replace("ё", "е")


def is_russian(word):
    return bool(re.fullmatch(r"[А-Яа-яЁё-]+", word))


def tokenize(text):
    return re.findall(r"[А-Яа-яЁё-]+|[0-9]+|[^\w\s]", text)
