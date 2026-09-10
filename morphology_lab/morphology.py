from functools import lru_cache
from preprocessing import norm

PRONOUNS = {"я","ты","он","она","оно","мы","вы","они","меня","тебя","его","ее","её","нас","вас","их","мне","тебе","ему","ей","нам","вам","им","мой","моя","мое","моё","мои","твой","твоя","твое","твоё","твои","наш","наша","наше","наши","ваш","ваша","ваше","ваши","этот","эта","это","эти","тот","та","то","те","кто","что","себя"}
PREPOSITIONS = {"в","во","на","под","над","за","из","изо","к","ко","от","до","для","без","при","по","о","об","обо","с","со","у","через","между"}
CONJUNCTIONS = {"и","а","но","или","либо"}
SUBORDINATING_CONJUNCTIONS = {"что","чтобы","если","когда","как","потому","поскольку","хотя"}
ADVERBS = {"очень","быстро","медленно","хорошо","плохо","сегодня","вчера","завтра","там","здесь","тут","всегда","никогда","снова","опять","уже","еще","ещё","только","почти","сразу","потом","затем","рядом","домой","внезапно","внимательно"}
NUMERALS = {"ноль","один","два","три","четыре","пять","шесть","семь","восемь","девять","десять","несколько","много"}

VERB_INFINITIVE_ENDINGS = ("ать","ять","ить","еть","оть","уть","ть","ти","чь")
REFLEXIVE_VERB_ENDINGS = ("алась","ялась","илась","елась","олась","улась","алось","ялось","илось","елось","олось","улось","ались","ялись","ились","елись","олись","улись","ался","ялся","ился","елся","олся","улся","лась","лось","лись","лся","ется","ится","ается","яется","ывается","ивается","увается","юется","тся","ться")
VERB_ENDINGS = ("ешь","ишь","ете","ите","ем","им","ет","ит","ут","ют","ат","ят","ла","ло","ли","л")
ADJ_ENDINGS = ("ого","его","ому","ему","ыми","ими","ых","их","ую","юю","ая","яя","ое","ее","ые","ие","ым","им","ой","ый","ий")

def has_ending(word, endings):
    return any(word.endswith(e) and len(word) > len(e) + 1 for e in endings)

@lru_cache(maxsize=100000)
def guess_pos(word):
    word = norm(word)
    if not word: return "X"
    if word in PREPOSITIONS: return "ADP"
    if word in CONJUNCTIONS: return "CCONJ"
    if word in SUBORDINATING_CONJUNCTIONS: return "SCONJ"
    if word in PRONOUNS: return "PRON"
    if word in ADVERBS: return "ADV"
    if word in NUMERALS: return "NUM"
    if has_ending(word, REFLEXIVE_VERB_ENDINGS): return "VERB"
    if has_ending(word, VERB_INFINITIVE_ENDINGS): return "VERB"
    if has_ending(word, VERB_ENDINGS): return "VERB"
    if has_ending(word, ADJ_ENDINGS): return "ADJ"
    return "NOUN"

@lru_cache(maxsize=100000)
def guess_lemma(word, pos):
    word = norm(word)
    if not word: return ""

    if pos == "VERB":
        if word.endswith(("ть","ти","чь")): return word

        reflexive = {
            "алась":"аться","ялась":"яться","илась":"иться","елась":"еться","олась":"оться","улась":"уться",
            "алось":"аться","ялось":"яться","илось":"иться","елось":"еться","олось":"оться","улось":"уться",
            "ались":"аться","ялись":"яться","ились":"иться","елись":"еться","олись":"оться","улись":"уться",
            "ался":"аться","ялся":"яться","ился":"иться","елся":"еться","олся":"оться","улся":"уться",
            "лась":"ться","лось":"ться","лись":"ться","лся":"ться","тся":"ться"
        }
        for ending, replacement in reflexive.items():
            if word.endswith(ending): return word[:-len(ending)] + replacement

        for ending in ("ла","ло","ли"):
            if word.endswith(ending): return word[:-2] + "ть"
        if word.endswith("л"): return word[:-1] + "ть"

        for ending in ("ешь","ишь","ете","ите","ем","им","ет","ит","ут","ют","ат","ят"):
            if word.endswith(ending): return word[:-len(ending)] + "ть"
        return word

    if pos == "ADJ":
        if word.endswith(("ый","ий","ой")): return word

        if word.endswith(("ая","ое","ые")):
            stem = word[:-2]
            return stem + ("ий" if stem.endswith("ск") else "ый")
        if word.endswith(("яя","ее","ие")): return word[:-2] + "ий"

        if word.endswith(("ого","ому","ых","ую","ым")):
            n = 3 if word.endswith(("ого","ому")) else 2
            stem = word[:-n]
            return stem + ("ий" if stem.endswith("ск") else "ый")
        if word.endswith("его"): return word[:-3] + "ий"
        if word.endswith("ему"): return word[:-3] + "ий"
        if word.endswith("ыми"):
            stem = word[:-4]
            return stem + ("ий" if stem.endswith("ск") else "ый")
        if word.endswith("ими"): return word[:-3] + "ий"
        if word.endswith("их"): return word[:-2] + "ий"
        if word.endswith("юю"): return word[:-2] + "ий"
        if word.endswith("им"): return word[:-2] + "ий"
        return word

    if pos == "NOUN":
        if word.endswith(("а","я","о","е")): return word

        if word.endswith("и") and len(word) > 3:
            stem = word[:-1]
            return stem + "а" if stem.endswith(("к","г","х","ц")) else stem
        if word.endswith("ы") and len(word) > 3: return word[:-1]
        if word.endswith(("ами","ями")): return word[:-4] + "а"
        if word.endswith(("ах","ях","ам","ям")): return word[:-2]
        if word.endswith(("ой","ей")): return word[:-2] + "а"
        if word.endswith(("ом","ем","ов","ев")): return word[:-2]
        if word.endswith(("у","ю")): return word[:-1]
        return word

    return word