from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

TRAIN_FILES = [
    DATA_DIR / "ru_syntagrus-ud-train-a.conllu",
    DATA_DIR / "ru_syntagrus-ud-train-b.conllu",
    DATA_DIR / "ru_syntagrus-ud-train-c.conllu"
]

TEST_FILE = DATA_DIR / "ru_syntagrus-ud-test.conllu"