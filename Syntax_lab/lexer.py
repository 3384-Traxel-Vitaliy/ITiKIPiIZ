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
    def __init__(self, token_type, value, position):
        self.type = token_type
        self.value = value
        self.position = position

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
        parsed = self.morph.parse(word)

        if parsed:
            return parsed[0].normal_form

        return word

    def find_terminal_form(self, word):
        word = word.lower()

        # Латинская c считается русской "с"
        if word == "c":
            return "с"

        all_terms = (
            COMMANDS
            | OBJECTS
            | DISH_TYPES
            | INGREDIENTS
            | CUISINES
            | COMPARISONS
            | CONJUNCTIONS
            | {WITH, KITCHEN, MINUTES}
        )

        if word in all_terms:
            return word

        normal = self.normalize_word(word)

        for term in all_terms:
            term_normal = self.normalize_word(term)

            if normal == term_normal:
                return term

        return word

    def classify_word(self, word):
        if word in COMMANDS:
            return "COMMAND"

        if word in {"рецепты", "блюда"}:
            return "OBJECT"

        if word in {"десерты", "супы", "салаты"}:
            return "OBJECT_OR_DISH_TYPE"

        if word in INGREDIENTS:
            return "INGREDIENT"

        if word in CUISINES:
            return "CUISINE"

        if word in COMPARISONS:
            return "COMPARISON"

        if word in CONJUNCTIONS:
            return "CONJUNCTION"

        if word in {"завтраки", "обеды", "ужины"}:
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
        words = re.findall(r"\S+", text.strip())
        tokens = []

        for position, original_word in enumerate(words):
            word = original_word.lower()

            terminal = self.find_terminal_form(word)
            token_type = self.classify_word(terminal)

            tokens.append(
                Token(
                    token_type,
                    terminal,
                    position
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