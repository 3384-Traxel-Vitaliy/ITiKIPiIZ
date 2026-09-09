import re
from functools import lru_cache


# Приводим слово к единому виду
@lru_cache(maxsize=200000)
def norm(word):
    return word.lower().replace("ё", "е")


# Проверяем, состоит ли слово из русских букв и дефиса
def is_russian(word):
    return bool(re.fullmatch(r"[А-Яа-яЁё-]+", word))


# Разбиваем текст на отдельные токены
def tokenize(text):
    return re.findall(
        r"[А-Яа-яЁё-]+|[0-9]+|[^\w\s]",
        text
    )