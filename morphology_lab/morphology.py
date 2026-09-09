from functools import lru_cache
from preprocessing import norm


# Списки слов для определения частей речи
ADVERBS = set("""
очень быстро медленно хорошо плохо сегодня вчера завтра
там здесь тут всегда никогда снова опять уже еще только
почти сразу потом затем
""".split())

PRONOUNS = set("""
я ты он она оно мы вы они меня тебя его ее её нас вас их
мне тебе ему ей нам вам им мой твой наш ваш этот эта это эти
""".split())

PREPOSITIONS = set("""
в во на под над за из изо к ко от до для без при по о об обо
с со у через между
""".split())

CONJUNCTIONS = set("""
и а но или либо что чтобы если когда как потому
""".split())


# Окончания используются для определения глаголов
VERB_ENDINGS = """
ться тся лась лось лись лся вший вшая вшее вшие
ющий ющая ющее ющие ящий ящая ящее ящие
ающий ающая ающее ающие яющий яющая яющее яющие
ла ло ли л ешь ишь ете ите ем им ет ит ут ют ат ят
""".split()

# Окончания для определения прилагательных
ADJ_ENDINGS = """
ого его ому ему ыми ими ых их ую юю
ая яя ое ее ые ие ым им ой ый ий
""".split()

# Частые суффиксы и окончания существительных
NOUN_ENDINGS = """
ость ение ание ия ие ство чик щик ник
ка ок ек ец ца
""".split()


def has_ending(word, endings):
    return any(
        word.endswith(x) and len(word) > len(x) + 1
        for x in endings
    )


@lru_cache(maxsize=100000)
def guess_pos(word):
    # Нормализуем слово перед анализом
    word = norm(word)

    groups = (
        (PREPOSITIONS, "ADP"),
        (CONJUNCTIONS, "CCONJ"),
        (PRONOUNS, "PRON"),
        (ADVERBS, "ADV")
    )

    # Сначала проверяем слова из готовых списков
    for words, pos in groups:
        if word in words:
            return pos

    # Затем определяем часть речи по окончаниям
    if has_ending(word, VERB_ENDINGS):
        return "VERB"

    if has_ending(word, ADJ_ENDINGS):
        return "ADJ"

    return "NOUN"


@lru_cache(maxsize=100000)
def guess_lemma(word, pos):
    # Нормализуем слово перед лемматизацией
    word = norm(word)

    # Определяем начальную форму глагола
    if pos == "VERB":
        reflexive = {
            "лась": "ться",
            "лось": "ться",
            "лись": "ться",
            "лся": "ться",
            "тся": "ться",
            "ются": "ться",
            "утся": "ться",
            "аются": "аться",
            "яются": "яться",
        }

        for ending, replacement in reflexive.items():
            if word.endswith(ending) and len(word) > len(ending) + 1:
                return word[:-len(ending)] + replacement

        endings = (
            "ющий", "ющая", "ющее", "ющие",
            "ящий", "ящая", "ящее", "ящие",
            "ающий", "ающая", "ающее", "ающие",
            "яющий", "яющая", "яющее", "яющие",
            "вший", "вшая", "вшее", "вшие",
            "ла", "ло", "ли", "л",
            "ешь", "ишь", "ете", "ите",
            "ем", "им", "ет", "ит",
            "ут", "ют", "ат", "ят",
        )

        for ending in endings:
            if word.endswith(ending) and len(word) > len(ending) + 1:
                return word[:-len(ending)] + "ть"

        return word

    # Восстанавливаем начальную форму прилагательного
    if pos == "ADJ":
        endings = (
            "ого", "его", "ому", "ему",
            "ыми", "ими", "ых", "их",
            "ую", "юю",
            "ая", "яя",
            "ое", "ее",
            "ые", "ие",
            "ым", "им",
            "ой", "ый", "ий",
        )

        for ending in endings:
            if not word.endswith(ending):
                continue

            # Если слово уже в начальной форме, оставляем его
            if ending in ("ый", "ий", "ой"):
                return word

            stem = word[:-len(ending)]

            # Восстанавливаем форму мужского рода
            if ending in ("ая", "яя"):
                if ending == "яя":
                    return stem + "ий"

                if stem.endswith("ск"):
                    return stem + "ий"

                return stem + "ый"

            if ending in ("ое", "ее", "ые", "ие"):
                if ending in ("ее", "ие"):
                    return stem + "ий"

                if stem.endswith("ск"):
                    return stem + "ий"

                return stem + "ый"

            if stem.endswith("ск"):
                return stem + "ий"

            return stem + "ый"

        return word

    # Восстанавливаем начальную форму существительного
    if pos == "NOUN":

        # Слова с этими окончаниями могут быть в начальной форме
        if word.endswith(("а", "я", "о", "е")):
            return word

        # Обработка формы множественного числа
        if word.endswith("и") and len(word) > 3:
            stem = word[:-1]

            if stem.endswith(("к", "г", "х", "ц")):
                return stem + "а"

            return stem

        if word.endswith("ы") and len(word) > 3:
            return word[:-1]

        # Обработка падежных окончаний
        if word.endswith(("ами", "ями")) and len(word) > 5:
            return word[:-3]

        if word.endswith(("ах", "ях")) and len(word) > 4:
            return word[:-2]

        if word.endswith(("ам", "ям")) and len(word) > 4:
            return word[:-2]

        if word.endswith("ой") and len(word) > 4:
            stem = word[:-2]
            return stem + "а"

        if word.endswith("ом") and len(word) > 4:
            return word[:-2]

        if word.endswith("ем") and len(word) > 4:
            return word[:-2]

        if word.endswith("ов") and len(word) > 4:
            return word[:-2]

        if word.endswith("ей") and len(word) > 4:
            return word[:-2]

        if word.endswith("у") and len(word) > 4:
            return word[:-1]

        if word.endswith("ю") and len(word) > 4:
            return word[:-1]

        # Дополнительные правила для неизвестных слов
        special_noun_patterns = {
            "вок": "вка",
            "век": "века",
            "нок": "нка",
        }

        for ending, replacement in special_noun_patterns.items():
            if word.endswith(ending) and len(word) > len(ending) + 2:
                return word[:-len(ending)] + replacement

        return word

    return word