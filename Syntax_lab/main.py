from lexer import Lexer
from parser import Parser
from errors import SyntaxError
from visualizer import TreeVisualizer


def process_query(query, lexer):
    print("=" * 70)
    print(f"Запрос: {query}")

    try:
        tokens = lexer.tokenize(query)

        parser = Parser(tokens)

        tree = parser.parse_query()

        print("Статус: УСПЕХ")
        print()
        print("Дерево:")

        TreeVisualizer.print_tree(tree)

    except SyntaxError as error:
        print("Статус: ОШИБКА")
        print(error)

    except Exception as error:
        print("Статус: ОШИБКА ПРОГРАММЫ")
        print(error)


def main():
    lexer = Lexer()

    try:
        with open(
            "input.txt",
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:
                query = line.strip()

                if not query:
                    continue

                process_query(
                    query,
                    lexer
                )

    except FileNotFoundError:
        print(
            "Ошибка: файл input.txt не найден."
        )


if __name__ == "__main__":
    main()