from config import TRAIN_FILES, TEST_FILE
from corpus import build_dictionary
from analyzer import MorphologicalAnalyzer
from tests import test_examples
from evaluation import evaluate


def run_variant(dictionary, name, use_levenshtein, use_morphology):
    analyzer = MorphologicalAnalyzer(dictionary, use_levenshtein=use_levenshtein, use_morphology=use_morphology)
    test_examples(analyzer, name)
    results = evaluate(analyzer, TEST_FILE, f"ОЦЕНКА: {name}")
    return analyzer, results


def interactive_check(analyzer):
    print("\n=== ИНТЕРАКТИВНАЯ ПРОВЕРКА ===")
    print("Введите предложение или exit для выхода.")

    while True:
        text = input("> ").strip()
        if text.lower() == "exit":
            break
        if not text:
            continue

        results = analyzer.analyze_text(text)
        print(" ".join(f"{word}{{{lemma}={pos}}}" for word, lemma, pos in results))


def print_comparison(results):
    print("\n=== СРАВНЕНИЕ ===")
    print(f"{'Вариант':28}{'Лемма':>10}{'POS':>10}{'Лемма+POS':>12}")
    print("-" * 60)

    for name, result in results:
        print(f"{name:28}{result['lemma']:9.2f}%{result['pos']:9.2f}%{result['joint']:11.2f}%")


def main():
    dictionary = build_dictionary(TRAIN_FILES)

    variants = [
        ("Только словарь", False, False),
        ("Словарь + Левенштейн", True, False),
        ("Левенштейн + морфология", True, True)
    ]

    all_results = []
    final_analyzer = None

    for name, use_levenshtein, use_morphology in variants:
        analyzer, results = run_variant(dictionary, name, use_levenshtein, use_morphology)
        all_results.append((name, results))
        final_analyzer = analyzer

    print_comparison(all_results)
    interactive_check(final_analyzer)


if __name__ == "__main__":
    main()