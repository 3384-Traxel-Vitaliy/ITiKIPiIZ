import re
import pymorphy3

from grammar import (
    COMMANDS,
    OBJECTS,
    DISH_TYPES,
    INGREDIENTS,
    CUISINES,
    COMPARISONS,
    CONJUNCTIONS,
    PREPOSITIONS,
    MINUTES,
    HOUR,
    KITCHEN,
    SEPARATORS
)


class Token:
    def __init__(
        self,
        token_type,
        value,
        position,
        original=None
    ):
        self.type = token_type
        self.value = value
        self.position = position
        self.original = (
            original
            if original is not None
            else value
        )

    def __repr__(self):
        return (
            f"Token("
            f"type='{self.type}', "
            f"value='{self.value}', "
            f"position={self.position})"
        )


class Lexer:
    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer()

    def normalize_word(self, word):
        word = word.lower()

        parsed = self.morph.parse(word)

        if parsed:
            return parsed[0].normal_form

        return word

    def classify_word(self, word):
        if word in COMMANDS:
            return "COMMAND"

        if word in OBJECTS:
            return "OBJECT"

        if word in DISH_TYPES:
            return "DISH_TYPE"

        if word in INGREDIENTS:
            return "INGREDIENT"

        if word in CUISINES:
            return "CUISINE"

        if word in COMPARISONS:
            return "COMPARISON"

        if word in CONJUNCTIONS:
            return "CONJUNCTION"

        if word in PREPOSITIONS:
            return "PREPOSITION"

        if word == KITCHEN:
            return "KITCHEN"

        if word == MINUTES:
            return "MINUTES"

        if word == HOUR:
            return "HOUR"

        if word in SEPARATORS:
            return "COMMA"

        if word.isdigit():
            return "NUMBER"

        return "UNKNOWN"

    def tokenize(self, text):
        words = re.findall(
            r"[А-Яа-яЁё]+|\d+|,",
            text.strip()
        )

        tokens = []

        for position, original_word in enumerate(words):

            if original_word == ",":
                normalized_word = ","
            else:
                normalized_word = self.normalize_word(
                    original_word
                )

            token_type = self.classify_word(
                normalized_word
            )

            tokens.append(
                Token(
                    token_type,
                    normalized_word,
                    position,
                    original_word
                )
            )

        tokens.append(
            Token(
                "EOF",
                "EOF",
                len(words)
            )
        )

        return tokens