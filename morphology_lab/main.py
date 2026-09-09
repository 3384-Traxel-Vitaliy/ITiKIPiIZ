from config import TRAIN_FILES, TEST_FILE
from corpus import build_dictionary
from analyzer import MorphologicalAnalyzer
from tests import test_examples
from evaluation import evaluate


def main():
    # Строим словарь по обучающему корпусу
    dictionary = build_dictionary(TRAIN_FILES)

    # Создаём морфологический анализатор
    analyzer = MorphologicalAnalyzer(dictionary)

    # Проверяем работу анализатора на тестовых предложениях
    print("\n=== ТЕСТОВЫЕ ПРЕДЛОЖЕНИЯ ===")
    test_examples(analyzer)

    # Оцениваем точность на тестовом корпусе
    print("\n=== ОЦЕНКА КОРПУСА ===")
    evaluate(analyzer, TEST_FILE)


if __name__ == "__main__":
    main()