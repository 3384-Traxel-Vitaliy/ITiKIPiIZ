from errors import SyntaxError

from nodes import (
    QueryNode,
    CommandNode,
    ObjectSpecNode,
    ObjectNode,
    FiltersNode,
    IngredientFilterNode,
    CuisineFilterNode,
    TimeFilterNode,
    TypeFilterNode,
    IngredientNode,
    CuisineNode,
    ComparisonNode,
    NumberNode,
    DishTypeNode,
    ConjunctionNode
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    @property
    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1

    def expect(self, token_type, message):
        token = self.current_token

        if token.type != token_type:
            raise SyntaxError(message, token)

        self.advance()
        return token

    def parse_query(self):
        command = self.parse_command()
        object_spec = self.parse_object_spec()

        if self.current_token.type != "EOF":
            raise SyntaxError(
                "Неожиданный токен после завершения запроса",
                self.current_token
            )

        return QueryNode(command, object_spec)

    def parse_command(self):
        token = self.expect(
            "COMMAND",
            "Ожидалась команда"
        )

        return CommandNode(token.value)

    def parse_object_spec(self):
        object_node = self.parse_object()

        # Фильтр обязателен
        filters = self.parse_filters()

        return ObjectSpecNode(
            object_node,
            filters
        )

    def parse_object(self):
        token = self.current_token

        if token.type == "OBJECT":
            self.advance()
            return ObjectNode(token.value)

        if token.type == "OBJECT_OR_DISH_TYPE":
            self.advance()
            return ObjectNode(token.value)

        raise SyntaxError(
            "Ожидался объект запроса",
            token
        )

    def parse_filters(self):
        children = []

        first_filter = self.parse_filter()
        children.append(first_filter)

        while True:
            # Фильтры с союзом:
            # с грибами и русской кухни
            if self.current_token.type == "CONJUNCTION":
                conjunction_token = self.current_token
                self.advance()

                children.append(
                    ConjunctionNode(
                        conjunction_token.value
                    )
                )

                next_filter = self.parse_filter()
                children.append(next_filter)

            # Последующий фильтр без союза:
            # русской кухни быстрее 40 минут
            elif self.current_token.type in {
                "WITH",
                "CUISINE",
                "COMPARISON",
                "DISH_TYPE",
                "OBJECT_OR_DISH_TYPE"
            }:
                next_filter = self.parse_filter()
                children.append(next_filter)

            else:
                break

        return FiltersNode(children)

    def parse_filter(self):
        token_type = self.current_token.type

        if token_type == "WITH":
            return self.parse_ingredient_filter()

        if token_type == "CUISINE":
            return self.parse_cuisine_filter()

        if token_type == "COMPARISON":
            return self.parse_time_filter()

        if token_type in {
            "DISH_TYPE",
            "OBJECT_OR_DISH_TYPE"
        }:
            return self.parse_type_filter()

        raise SyntaxError(
            "Ожидался фильтр",
            self.current_token
        )

    def parse_ingredient_filter(self):
        self.expect(
            "WITH",
            "Ожидалось 'с'"
        )

        token = self.expect(
            "INGREDIENT",
            "Ожидался ингредиент"
        )

        ingredient = IngredientNode(token.value)

        return IngredientFilterNode(ingredient)

    def parse_cuisine_filter(self):
        cuisine_token = self.expect(
            "CUISINE",
            "Ожидалось название кухни"
        )

        self.expect(
            "KITCHEN",
            "Ожидалось слово 'кухни'"
        )

        cuisine = CuisineNode(cuisine_token.value)

        return CuisineFilterNode(cuisine)

    def parse_time_filter(self):
        comparison_token = self.expect(
            "COMPARISON",
            "Ожидалось сравнение"
        )

        number_token = self.expect(
            "NUMBER",
            "Ожидалось число"
        )

        self.expect(
            "MINUTES",
            "Ожидалось слово 'минут'"
        )

        comparison = ComparisonNode(
            comparison_token.value
        )

        number = NumberNode(
            number_token.value
        )

        return TimeFilterNode(
            comparison,
            number
        )

    def parse_type_filter(self):
        token = self.current_token

        if token.type not in {
            "DISH_TYPE",
            "OBJECT_OR_DISH_TYPE"
        }:
            raise SyntaxError(
                "Ожидался тип блюда",
                token
            )

        self.advance()

        dish_type = DishTypeNode(
            token.value
        )

        return TypeFilterNode(dish_type)