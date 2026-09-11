class TreeVisualizer:

    @staticmethod
    def print_tree(node):
        print(
            node.name,
            end=""
        )

        if node.value is not None:
            print(
                f": {node.value}"
            )
        else:
            print()

        TreeVisualizer._print_children(
            node.children,
            ""
        )

    @staticmethod
    def _print_children(
        children,
        prefix
    ):
        for index, child in enumerate(children):
            is_last = (
                index == len(children) - 1
            )

            if is_last:
                branch = "└── "
                next_prefix = prefix + "    "
            else:
                branch = "├── "
                next_prefix = prefix + "│   "

            print(
                prefix + branch + child.name,
                end=""
            )

            if child.value is not None:
                print(
                    f": {child.value}"
                )
            else:
                print()

            TreeVisualizer._print_children(
                child.children,
                next_prefix
            )