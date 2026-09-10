import re

from preprocessing import norm, tokenize, is_russian
from morphology import guess_pos, guess_lemma
from similarity import find_similar


class MorphologicalAnalyzer:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.word_index = self._build_index()
        self.cache = {}

    def _build_index(self):
        # Создаём индекс слов для быстрого поиска
        from similarity import build_word_index
        return build_word_index(self.dictionary)

    @staticmethod
    def _has_latin(word):
        """
        Проверяет, содержит ли слово хотя бы одну латинскую букву.
        """
        return bool(re.search(r"[A-Za-z]", word))

    def analyze_unknown(self, word):
        original = word
        word = norm(word)

        # Пустое слово не анализируем
        if not word:
            return "", "X"

        # Если слово содержит латиницу, считаем его неизвестной частью речи X
        if self._has_latin(original):
            return word, "X"

        # Определяем часть речи и предполагаемую лемму
        pos = guess_pos(word)
        lemma = guess_lemma(word, pos)

        # Для некоторых частей речи используем результат правил
        if (
            pos in ("VERB", "ADJ")
            or word.endswith(("ость", "ение", "ание", "ство"))
        ):
            return lemma, pos

        # Ищем похожее слово в словаре
        similar = find_similar(
            word,
            self.word_index
        )

        if similar:
            for candidate, _ in similar:
                variants = [
                    (lp, count)
                    for lp, count in self.dictionary[candidate].items()
                    if lp[1] == pos
                ]

                if variants:
                    return max(
                        variants,
                        key=lambda x: x[1]
                    )[0]

            # Если точного варианта по POS нет, берём самый частый вариант
            return self.dictionary[
                similar[0][0]
            ].most_common(1)[0][0]

        # Слово с заглавной буквы считаем именем собственным
        if original[0].isupper() and pos == "NOUN":
            return word, "PROPN"

        return lemma, pos

    def analyze_word(self, word):
        # Используем сохранённый результат, если он уже есть
        if word in self.cache:
            return self.cache[word]

        # Если слово содержит латинские буквы, сразу определяем его как X
        if self._has_latin(word):
            result = (word, "X")

            self.cache[word] = result
            return result

        if word.isdigit():
            return word, "NUM"

        normalized = norm(word)

        # Пустое слово
        if not normalized:
            result = ("", "X")

            self.cache[word] = result
            return result

        # Сначала ищем слово непосредственно в словаре
        if normalized in self.dictionary:
            result = self.dictionary[
                normalized
            ].most_common(1)[0][0]

        else:
            # Если слова нет, применяем правила анализа
            result = self.analyze_unknown(word)

        self.cache[word] = result
        return result

    def analyze_text(self, text):
        result = []

        for token in tokenize(text):

            # Латиница - X
            if self._has_latin(token):
                result.append(
                    (token, token, "X")
                )
                continue

            # Русские токены - обычный морфологический анализ
            if is_russian(token):
                result.append(
                    (token, *self.analyze_word(token))
                )

        return result