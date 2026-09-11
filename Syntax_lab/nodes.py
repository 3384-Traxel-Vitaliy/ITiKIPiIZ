class Node:
    def __init__(
        self,
        name,
        value=None,
        children=None
    ):
        self.name = name
        self.value = value
        self.children = (
            children
            if children is not None
            else []
        )

    def add_child(self, child):
        self.children.append(child)


class QueryNode(Node):
    def __init__(self, command, object_spec):
        super().__init__(
            "Query",
            children=[
                command,
                object_spec
            ]
        )


class CommandNode(Node):
    def __init__(self, value):
        super().__init__(
            "Command",
            value
        )


class ObjectSpecNode(Node):
    def __init__(
        self,
        object_node,
        filters
    ):
        super().__init__(
            "ObjectSpec",
            children=[
                object_node,
                filters
            ]
        )


class ObjectNode(Node):
    def __init__(self, value):
        super().__init__(
            "Object",
            value
        )


class FiltersNode(Node):
    def __init__(self, children=None):
        super().__init__(
            "Filters",
            children=children
        )


class IngredientCuisineFilterNode(Node):
    def __init__(
        self,
        ingredient_group,
        cuisine_filter=None,
        time_filter=None
    ):
        children = [
            ingredient_group
        ]

        if cuisine_filter is not None:
            children.append(
                cuisine_filter
            )

        if time_filter is not None:
            children.append(
                time_filter
            )

        super().__init__(
            "IngredientCuisineFilter",
            children=children
        )


class IngredientGroupNode(Node):
    def __init__(self, children=None):
        super().__init__(
            "IngredientGroup",
            children=children
        )


class IngredientFilterNode(Node):
    def __init__(self, ingredient):
        super().__init__(
            "IngredientFilter",
            children=[ingredient]
        )


class CuisineFilterNode(Node):
    def __init__(self, cuisine):
        super().__init__(
            "CuisineFilter",
            children=[cuisine]
        )


class TimeFilterNode(Node):
    def __init__(
        self,
        comparison,
        hours=None,
        minutes=None
    ):
        children = [
            comparison
        ]

        if hours is not None:
            children.append(hours)

        if minutes is not None:
            children.append(minutes)

        super().__init__(
            "TimeFilter",
            children=children
        )


class TypeFilterNode(Node):
    def __init__(self, dish_type):
        super().__init__(
            "TypeFilter",
            children=[dish_type]
        )


class IngredientNode(Node):
    def __init__(self, value):
        super().__init__(
            "Ingredient",
            value
        )


class CuisineNode(Node):
    def __init__(self, value):
        super().__init__(
            "Cuisine",
            value
        )


class ComparisonNode(Node):
    def __init__(self, value):
        super().__init__(
            "Comparison",
            value
        )


class NumberNode(Node):
    def __init__(self, value):
        super().__init__(
            "Number",
            value
        )


class HourNode(Node):
    def __init__(self, value):
        super().__init__(
            "Hour",
            value
        )


class DishTypeNode(Node):
    def __init__(self, value):
        super().__init__(
            "DishType",
            value
        )


class ConjunctionNode(Node):
    def __init__(self, value):
        super().__init__(
            "Conjunction",
            value
        )
