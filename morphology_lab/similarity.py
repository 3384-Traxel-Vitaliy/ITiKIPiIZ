from collections import defaultdict
from functools import lru_cache
from preprocessing import norm


def build_word_index(dictionary):
    index = defaultdict(list)
    for word in dictionary:
        if word:
            index[(word[0], len(word))].append(word)
    return index


@lru_cache(maxsize=200000)
def levenshtein_one(a, b):
    if a == b:
        return 0

    len_a, len_b = len(a), len(b)
    if abs(len_a - len_b) > 1:
        return 2

    if len_a == len_b:
        differences = sum(char_a != char_b for char_a, char_b in zip(a, b))
        return 2 if differences > 1 else differences

    if len_a < len_b:
        a, b = b, a
        len_a, len_b = len_b, len_a

    i = j = differences = 0

    while i < len_a and j < len_b:
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            differences += 1
            if differences > 1:
                return 2
            i += 1

    return 1


def find_similar(word, word_index, max_distance=1, limit=5):
    word = norm(word)
    if not word:
        return []

    length, first_letter = len(word), word[0]
    candidates = []

    for candidate_length in (length - 1, length, length + 1):
        if candidate_length <= 0:
            continue

        for candidate in word_index.get((first_letter, candidate_length), ()):
            distance = levenshtein_one(word, candidate)
            if distance <= max_distance:
                candidates.append((candidate, distance))

    candidates.sort(key=lambda item: item[1])
    return candidates[:limit]
