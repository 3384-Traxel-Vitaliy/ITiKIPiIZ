from collections import defaultdict, Counter
from preprocessing import norm


def read_conllu(filename):
    data = []
    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")
            if len(parts) < 4:
                continue

            token_id = parts[0]
            if "-" in token_id or "." in token_id:
                continue

            form, lemma, pos = parts[1:4]
            if form and lemma and pos:
                data.append((form, lemma, pos))

    return data


def build_dictionary(files):
    dictionary = defaultdict(Counter)
    total = 0

    for filename in files:
        print("Читаем:", filename)
        for form, lemma, pos in read_conllu(filename):
            dictionary[norm(form)][(norm(lemma), pos)] += 1
            total += 1

    print(f"Обработано токенов: {total}")
    print(f"Размер словаря: {len(dictionary)}")
    return dictionary