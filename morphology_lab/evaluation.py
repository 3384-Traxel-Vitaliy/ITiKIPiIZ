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

    # Сохраняем максимум 50 ошибок
    errors = []

    # Сравниваем предсказания с правильными значениями
    for form, true_lemma, true_pos in data:
        pred_lemma, pred_pos = predictions[form]

        lemma_ok = norm(pred_lemma) == norm(true_lemma)
        pos_ok = pred_pos == true_pos

        lemma_correct += lemma_ok
        pos_correct += pos_ok
        joint_correct += lemma_ok and pos_ok

        # Сохраняем ошибку
        if not (lemma_ok and pos_ok) and len(errors) < 50:
            errors.append(
                (form, true_lemma, true_pos, pred_lemma, pred_pos)
            )

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

    # Выводим ошибки компактно
    print("\n=== ОШИБКИ (макс. 50) ===")

    if errors:
        for word, true_lemma, true_pos, pred_lemma, pred_pos in errors:
            print(
                f"{word} → {true_lemma}/{true_pos} | "
                f"{pred_lemma}/{pred_pos}"
            )
    else:
        print("Ошибок не найдено.")

    return results