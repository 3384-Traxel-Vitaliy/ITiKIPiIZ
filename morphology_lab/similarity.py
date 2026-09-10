from collections import defaultdict
from functools import lru_cache
from preprocessing import norm


def build_word_index(dictionary):
    # Индексируем слова по первой букве и длине
    index = defaultdict(list)

    for word in dictionary:
        if word:
            index[(word[0], len(word))].append(word)

    return index


@lru_cache(maxsize=200000)
def levenshtein(a, b):
    # Одинаковые слова
    if a == b:
        return 0

    # Пустые слова
    if not a:
        return len(b)

    if not b:
        return len(a)

    # При расстоянии 1 длина должна отличаться
    # не более чем на один символ
    if abs(len(a) - len(b)) > 1:
        return 2

    # Короткое слово помещаем в b
    if len(a) < len(b):
        a, b = b, a

    # Вместо полной матрицы считаем только
    # три соседние диагонали
    previous = list(range(len(b) + 1))

    for i, char_a in enumerate(a, 1):
        current = [2] * (len(b) + 1)

        # Начальное значение
        current[0] = i

        # При расстоянии 1 смотрим только соседние позиции
        start = max(1, i - 1)
        end = min(len(b), i + 1)

        for j in range(start, end + 1):
            current[j] = min(
                current[j - 1] + 1,
                previous[j] + 1,
                previous[j - 1] + (char_a != b[j - 1])
            )

        # Если минимальное расстояние в строке уже больше 1,
        # дальнейший расчёт не нужен
        if min(current[start:end + 1]) > 1:
            return 2

        previous = current

    return previous[len(b)]


def find_similar(word, word_index, max_distance=1, limit=5):
    # Нормализуем слово
    word = norm(word)

    if not word:
        return []

    word_length = len(word)
    first_letter = word[0]

    candidates = []

    # При max_distance=1 проверяем только три длины
    min_length = max(1, word_length - max_distance)
    max_length = word_length + max_distance

    for length in range(min_length, max_length + 1):

        # Берём только слова с такой же первой буквой
        for candidate in word_index.get(
            (first_letter, length),
            ()
        ):
            distance = levenshtein(word, candidate)

            if distance <= max_distance:
                candidates.append((candidate, distance))

    if not candidates:
        return []

    candidates.sort(key=lambda x: x[1])

    return candidates[:limit]
