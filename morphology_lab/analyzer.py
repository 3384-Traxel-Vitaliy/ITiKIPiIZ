import re
from preprocessing import norm, tokenize


class MorphologicalAnalyzer:
    def __init__(self, dictionary, use_levenshtein=False, use_morphology=False):
        self.dictionary = dictionary
        self.use_levenshtein = use_levenshtein
        self.use_morphology = use_morphology
        self.cache = {}

        if use_levenshtein:
            from similarity import build_word_index
            self.word_index = build_word_index(dictionary)
        else:
            self.word_index = None

    @staticmethod
    def has_latin(word):
        return bool(re.search(r"[A-Za-z]", word))

    def analyze_word(self, word):
        if self.has_latin(word):
            result = (word, "X")
            self.cache[word] = result
            return result

        if word.isdigit():
            result = (word, "NUM")
            self.cache[word] = result
            return result

        if word in self.cache:
            return self.cache[word]

        normalized = norm(word)
        if not normalized:
            result = ("", "X")
            self.cache[word] = result
            return result

        if normalized in self.dictionary:
            result = self.dictionary[normalized].most_common(1)[0][0]
            self.cache[word] = result
            return result

        if self.use_morphology:
            from morphology import guess_pos, guess_lemma
            pos = guess_pos(normalized)

            if pos != "NOUN":
                result = (guess_lemma(normalized, pos), pos)
                self.cache[word] = result
                return result

        if self.use_levenshtein:
            from similarity import find_similar
            similar = find_similar(normalized, self.word_index)

            if similar:
                candidate = similar[0][0]
                result = self.dictionary[candidate].most_common(1)[0][0]
                self.cache[word] = result
                return result

        if self.use_morphology:
            from morphology import guess_pos, guess_lemma
            pos = guess_pos(normalized)
            result = (guess_lemma(normalized, pos), pos)
            self.cache[word] = result
            return result

        result = (normalized, "X")
        self.cache[word] = result
        return result

    def analyze_text(self, text):
        result = []
        for token in tokenize(text):
            if not any(char.isalnum() for char in token):
                continue
            lemma, pos = self.analyze_word(token)
            result.append((token, lemma, pos))
        return result
