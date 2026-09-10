from tqdm.auto import tqdm
from preprocessing import norm
from corpus import read_conllu


def evaluate(analyzer, filename):
    # Загружаем данные тестового корпуса
    data = read_conllu(filename)

    # Получаем уникальные слова для анализа
    unique_words = {form for form, _, _ in data}

    # Анализируем каждое слово один раз
    predictions = {
        word: analyzer.analyze_word(word)
        for word in tqdm(unique_words, desc="Анализ слов")
    }

    lemma_correct = 0
    pos_correct = 0
    joint_correct = 0

    # Отдельные категории ошибок
    lemma_errors = []       # лемма неверная, POS верный
    pos_errors = []         # лемма верная, POS неверный
    joint_errors = []       # лемма и POS неверные

    # Сравниваем предсказания с правильными значениями
    for form, true_lemma, true_pos in data:
        pred_lemma, pred_pos = predictions[form]

        lemma_ok = norm(pred_lemma) == norm(true_lemma)
        pos_ok = pred_pos == true_pos

        lemma_correct += lemma_ok
        pos_correct += pos_ok
        joint_correct += lemma_ok and pos_ok

        error = (form, true_lemma, true_pos, pred_lemma, pred_pos)

        # Раскладываем ошибки по категориям
        if not lemma_ok and pos_ok:
            lemma_errors.append(error)

        elif lemma_ok and not pos_ok:
            pos_errors.append(error)

        elif not lemma_ok and not pos_ok:
            joint_errors.append(error)

    total = len(data)

    # Рассчитываем точность
    results = {
        "lemma": lemma_correct / total * 100,
        "pos": pos_correct / total * 100,
        "joint": joint_correct / total * 100
    }

    print(f"Лемма: {results['lemma']:.2f}%")
    print(f"POS: {results['pos']:.2f}%")
    print(f"Лемма + POS: {results['joint']:.2f}%")

    def print_errors(title, errors, limit=20):
        print(f"\n=== {title} (макс. {limit}) ===")

        if errors:
            for word, true_lemma, true_pos, pred_lemma, pred_pos in errors[:limit]:
                print(
                    f"{word} → {true_lemma}/{true_pos} | "
                    f"{pred_lemma}/{pred_pos}"
                )
        else:
            print("Ошибок не найдено.")

    # Сначала 20 ошибок только по лемме
    print_errors(
        "ОШИБКИ: НЕ СОВПАДАЕТ ЛЕММА, POS ВЕРНЫЙ",
        lemma_errors
    )

    # Затем 20 ошибок только по POS
    print_errors(
        "ОШИБКИ: ЛЕММА ВЕРНА, НЕ СОВПАДАЕТ POS",
        pos_errors
    )

    # Затем 20 ошибок, где неверны и лемма, и POS
    print_errors(
        "ОШИБКИ: НЕ СОВПАДАЮТ ЛЕММА И POS",
        joint_errors
    )

    return results