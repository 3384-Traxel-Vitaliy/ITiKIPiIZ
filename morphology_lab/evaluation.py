from tqdm.auto import tqdm
from preprocessing import norm
from corpus import read_conllu


def evaluate(analyzer, filename, title):
    data = read_conllu(filename)
    unique_words = {form for form, _, _ in data}
    predictions = {
        word: analyzer.analyze_word(word)
        for word in tqdm(unique_words, desc=f"Анализ: {title}")
    }

    lemma_correct = pos_correct = joint_correct = 0
    lemma_errors, pos_errors, joint_errors = [], [], []

    for form, true_lemma, true_pos in data:
        pred_lemma, pred_pos = predictions[form]
        lemma_ok = norm(pred_lemma) == norm(true_lemma)
        pos_ok = pred_pos == true_pos

        lemma_correct += lemma_ok
        pos_correct += pos_ok
        joint_correct += lemma_ok and pos_ok

        error = (form, true_lemma, true_pos, pred_lemma, pred_pos)
        if not lemma_ok and pos_ok:
            lemma_errors.append(error)
        elif lemma_ok and not pos_ok:
            pos_errors.append(error)
        elif not lemma_ok and not pos_ok:
            joint_errors.append(error)

    total = len(data)
    results = {
        "lemma": lemma_correct / total * 100,
        "pos": pos_correct / total * 100,
        "joint": joint_correct / total * 100
    }

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(f"Лемма: {results['lemma']:.2f}%")
    print(f"POS: {results['pos']:.2f}%")
    print(f"Лемма + POS: {results['joint']:.2f}%")

    def print_errors(title, errors, limit=20):
        print(f"\n=== {title} (макс. {limit}) ===")
        if not errors:
            print("Ошибок не найдено.")
            return

        for word, true_lemma, true_pos, pred_lemma, pred_pos in errors[:limit]:
            print(f"{word} → {true_lemma}/{true_pos} | {pred_lemma}/{pred_pos}")

    print_errors("ОШИБКИ: НЕВЕРНА ЛЕММА, POS ВЕРНЫЙ", lemma_errors)
    print_errors("ОШИБКИ: ЛЕММА ВЕРНА, POS НЕВЕРНЫЙ", pos_errors)
    print_errors("ОШИБКИ: НЕВЕРНЫ ЛЕММА И POS", joint_errors)

    return results