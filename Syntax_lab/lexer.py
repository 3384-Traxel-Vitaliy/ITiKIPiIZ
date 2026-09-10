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
    MINUTES,
    WITH,
    KITCHEN
)


class Token:
    def __init__(self, token_type, value, position, original=None):
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

        if word in {"рецепт", "блюдо"}:
            return "OBJECT"

        # Эти слова могут выступать как объект или как тип блюда.
        if word in {"десерт", "суп", "салат"}:
            return "OBJECT_OR_DISH_TYPE"

        if word in INGREDIENTS:
            return "INGREDIENT"

        if word in CUISINES:
            return "CUISINE"

        if word in COMPARISONS:
            return "COMPARISON"

        if word in CONJUNCTIONS:
            return "CONJUNCTION"

        if word in {"завтрак", "обед", "ужин"}:
            return "DISH_TYPE"

        if word == WITH:
            return "WITH"

        if word == KITCHEN:
            return "KITCHEN"

        if word == MINUTES:
            return "MINUTES"

        if word.isdigit():
            return "NUMBER"

        return "UNKNOWN"

    def tokenize(self, text):

        words = re.findall(
            r"\S+",
            text.strip()
        )

        tokens = []

        for position, original_word in enumerate(words):

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