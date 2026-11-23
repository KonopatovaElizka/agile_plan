
import json
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "tasks.json"


def save_tasks(tasks):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def load_tasks():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
