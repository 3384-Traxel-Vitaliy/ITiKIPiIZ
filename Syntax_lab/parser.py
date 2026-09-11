from errors import SyntaxError

from nodes import (
    Node,
    QueryNode,
    CommandNode,
    ObjectSpecNode,
    ObjectNode,
    FiltersNode,
    IngredientCuisineFilterNode,
    IngredientGroupNode,
    IngredientFilterNode,
    CuisineFilterNode,
    TimeFilterNode,
    TypeFilterNode,
    IngredientNode,
    CuisineNode,
    ComparisonNode,
    NumberNode,
    DishTypeNode,
    ConjunctionNode,
    HourNode
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
            raise SyntaxError(
                message,
                token
            )

        self.advance()

        return token

    def parse_query(self):
        """
        <query> ::= <command> <object_spec>
        """

        command = self.parse_command()

        object_spec = self.parse_object_spec()

        if self.current_token.type != "EOF":
            raise SyntaxError(
                "Неожиданный токен после завершения запроса",
                self.current_token
            )

        return QueryNode(
            command,
            object_spec
        )

    def parse_command(self):
        """
        <command> ::= "найти" | "показать" | "вывести"
        """

        token = self.expect(
            "COMMAND",
            "Ожидалась команда"
        )

        return CommandNode(
            token.value
        )

    def parse_object_spec(self):
        """
        <object_spec> ::= <object> <filters> | <dish_type> <filters>
        """

        if self.current_token.type == "OBJECT":
            object_node = self.parse_object()

        elif self.current_token.type == "DISH_TYPE":
            object_node = self.parse_object_dish_type()

        else:
            raise SyntaxError(
                "Ожидался объект или тип блюда",
                self.current_token
            )

        filters = self.parse_filters()

        return ObjectSpecNode(
            object_node,
            filters
        )

    def parse_object(self):
        """
        <object> ::= "рецепт" | "блюдо" | "список"
        """

        token = self.expect(
            "OBJECT",
            "Ожидался объект запроса"
        )

        return ObjectNode(
            token.value
        )

    def parse_object_dish_type(self):
        """
        <dish_type> непосредственно после команды.
        """

        token = self.expect(
            "DISH_TYPE",
            "Ожидался тип блюда"
        )

        return DishTypeNode(
            token.value
        )

    def parse_filters(self):
        """
        <filters> ::= <ingredient_cuisine_filter> | <cuisine_time_filter> | <other_filter>
        """

        if self.current_token.type == "PREPOSITION":
            first_filter = (
                self.parse_ingredient_cuisine_filter()
            )

        elif self.current_token.type == "CUISINE":
            first_filter = (
                self.parse_cuisine_time_filter()
            )

        elif self.current_token.type in {
            "COMPARISON",
            "DISH_TYPE"
        }:
            first_filter = (
                self.parse_other_filter()
            )

        else:
            raise SyntaxError(
                "Ожидался фильтр",
                self.current_token
            )

        return FiltersNode(
            [first_filter]
        )

    def parse_ingredient_cuisine_filter(self):
        """
        <ingredient_cuisine_filter> ::= <ingredient_filter> <ingredient_tail> <cuisine_opt> <time_opt>
        """

        first_ingredient = (
            self.parse_ingredient_filter()
        )

        ingredients = [
            first_ingredient
        ]

        self.parse_ingredient_tail(
            ingredients
        )

        ingredient_group = IngredientGroupNode(
            ingredients
        )

        cuisine_filter = None

        if self.current_token.type == "CUISINE":
            cuisine_filter = (
                self.parse_cuisine_filter()
            )

        time_filter = None

        if self.current_token.type == "COMPARISON":
            time_filter = (
                self.parse_time_filter()
            )

        return IngredientCuisineFilterNode(
            ingredient_group,
            cuisine_filter,
            time_filter
        )

    def parse_ingredient_tail(self, children):
        """
        <ingredient_tail> ::= <ingredient_separator> <ingredient> <ingredient_tail> | ε
        """

        while self.current_token.type in {
            "CONJUNCTION",
            "COMMA"
        }:

            separator_token = (
                self.current_token
            )

            self.advance()

            children.append(
                ConjunctionNode(
                    separator_token.value
                )
            )

            ingredient_token = self.expect(
                "INGREDIENT",
                "Ожидался ингредиент после разделителя"
            )

            children.append(
                IngredientFilterNode(
                    IngredientNode(
                        ingredient_token.value
                    )
                )
            )

    def parse_cuisine_time_filter(self):
        """
        <cuisine_time_filter> ::= <cuisine_filter> <time_opt>
        """

        cuisine_filter = (
            self.parse_cuisine_filter()
        )

        time_filter = None

        if self.current_token.type == "COMPARISON":
            time_filter = (
                self.parse_time_filter()
            )

        children = [
            cuisine_filter
        ]

        if time_filter is not None:
            children.append(
                time_filter
            )

        return Node(
            "CuisineTimeFilter",
            children=children
        )

    def parse_other_filter(self):
        """
        <other_filter> ::= <time_filter> | <type_filter>
        """

        if self.current_token.type == "COMPARISON":
            return self.parse_time_filter()

        if self.current_token.type == "DISH_TYPE":
            return self.parse_type_filter()

        raise SyntaxError(
            "Ожидался фильтр времени или тип блюда",
            self.current_token
        )

    def parse_ingredient_filter(self):
        """
        <ingredient_filter> ::= <preposition> <ingredient>
        """

        self.expect(
            "PREPOSITION",
            "Ожидался предлог 'с' или 'из'"
        )

        token = self.expect(
            "INGREDIENT",
            "Ожидался ингредиент"
        )

        ingredient = IngredientNode(
            token.value
        )

        return IngredientFilterNode(
            ingredient
        )

    def parse_cuisine_filter(self):
        """
        <cuisine_filter> ::= <cuisine> "кухня"
        """

        cuisine_token = self.expect(
            "CUISINE",
            "Ожидалось название кухни"
        )

        self.expect(
            "KITCHEN",
            "Ожидалось слово 'кухня'"
        )

        cuisine = CuisineNode(
            cuisine_token.value
        )

        return CuisineFilterNode(
            cuisine
        )

    def parse_time_filter(self):
        """
        <time_filter> ::= <comparison> <number> <time_unit>

        <time_unit> ::= "минута" | "час" <minutes_opt>

        <minutes_opt> ::= <number> "минута" | ε
        """

        comparison_token = self.expect(
            "COMPARISON",
            "Ожидалось сравнение"
        )

        comparison = ComparisonNode(
            comparison_token.value
        )

        number_token = self.expect(
            "NUMBER",
            "Ожидалось число"
        )

        if self.current_token.type == "MINUTES":
            self.advance()

            minutes = NumberNode(
                number_token.value
            )

            return TimeFilterNode(
                comparison,
                minutes=minutes
            )

        if self.current_token.type == "HOUR":
            self.advance()

            hours = HourNode(
                number_token.value
            )

            minutes = (
                self.parse_optional_minutes()
            )

            return TimeFilterNode(
                comparison,
                hours=hours,
                minutes=minutes
            )

        raise SyntaxError(
            "Ожидалось слово 'минута' или 'час'",
            self.current_token
        )

    def parse_optional_minutes(self):
        """
        <minutes_opt> ::= <number> "минута" | ε
        """

        if self.current_token.type != "NUMBER":
            return None

        number_token = self.current_token

        self.advance()

        self.expect(
            "MINUTES",
            "Ожидалось слово 'минута'"
        )

        return NumberNode(
            number_token.value
        )

    def parse_type_filter(self):
        """
        <type_filter> ::= <dish_type>
        """

        token = self.expect(
            "DISH_TYPE",
            "Ожидался тип блюда"
        )

        dish_type = DishTypeNode(
            token.value
        )

        return TypeFilterNode(
            dish_type
        )
