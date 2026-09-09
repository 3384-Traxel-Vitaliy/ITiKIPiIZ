from tqdm.auto import tqdm
from preprocessing import norm
from corpus import read_conllu


def evaluate(analyzer, filename):
    # Загружаем данные тестового корпуса
    data = read_conllu(filename)

    # Получаем уникальные слова для анализа
    unique_words = {
        form for form, _, _ in data
    }

    # Анализируем каждое слово один раз
    predictions = {
        word: analyzer.analyze_word(word)
        for word in tqdm(
            unique_words,
            desc="Анализ слов"
        )
    }

    lemma_correct = 0
    pos_correct = 0
    joint_correct = 0

    # Сравниваем предсказания с правильными значениями
    for form, true_lemma, true_pos in data:
        pred_lemma, pred_pos = predictions[form]

        lemma_ok = norm(pred_lemma) == norm(true_lemma)
        pos_ok = pred_pos == true_pos

        lemma_correct += lemma_ok
        pos_correct += pos_ok
        joint_correct += lemma_ok and pos_ok

    total = len(data)

    # Рассчитываем точность анализа
    results = {
        "lemma": lemma_correct / total * 100,
        "pos": pos_correct / total * 100,
        "joint": joint_correct / total * 100
    }

    print(f"Лемма: {results['lemma']:.2f}%")
    print(f"POS: {results['pos']:.2f}%")
    print(f"Лемма + POS: {results['joint']:.2f}%")

    return results