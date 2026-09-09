from collections import defaultdict
from functools import lru_cache
from preprocessing import norm


def build_word_index(dictionary):
    # Создаём индекс слов по первой букве и длине
    index = defaultdict(list)

    for word in dictionary:
        if word:
            index[(word[0], len(word))].append(word)

    return index


@lru_cache(maxsize=100000)
def levenshtein(a, b):
    # Если слова одинаковые, расстояние равно нулю
    if a == b:
        return 0

    if not a:
        return len(b)

    if not b:
        return len(a)

    if len(a) < len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))

    # Вычисляем расстояние Левенштейна
    for i, char_a in enumerate(a, 1):
        current = [i]

        for j, char_b in enumerate(b, 1):
            current.append(min(
                current[j - 1] + 1,
                previous[j] + 1,
                previous[j - 1] + (char_a != char_b)
            ))

        previous = current

    return previous[-1]


def find_similar(word, word_index, max_distance=1, limit=5):
    # Нормализуем искомое слово
    word = norm(word)

    if not word:
        return []

    candidates = []

    # Ищем слова близкой длины
    for length in range(
        max(1, len(word) - max_distance),
        len(word) + max_distance + 1
    ):
        for candidate in word_index.get(
            (word[0], length), ()
        ):
            distance = levenshtein(word, candidate)

            if distance <= max_distance:
                candidates.append((candidate, distance))

    # Сортируем по степени похожести
    candidates.sort(
        key=lambda x: (
            x[1],
            abs(len(x[0]) - len(word))
        )
    )

    return candidates[:limit]