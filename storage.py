import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "tujuStorage.json")

VALID_FIELDS = ("mood", "reason", "tempo", "fuel")


def _ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def _today_key():
    return datetime.now().strftime("%d-%b-%Y")


def load_data():
    _ensure_storage()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    _ensure_storage()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_data_to_file(data_name, data_from_input):
    """Mirrors the original Android app's Functions.addDataToFile:
    appends a value under today's date, grouped by mood/reason/tempo/fuel."""
    data_name = data_name.lower()
    if data_name not in VALID_FIELDS:
        raise ValueError("Options for data_name are: mood, reason, tempo or fuel.")

    data = load_data()
    today = _today_key()

    day_data = data.get(today, {"mood": [], "reason": [], "tempo": [], "fuel": []})
    day_data.setdefault(data_name, [])
    day_data[data_name].append(data_from_input)
    data[today] = day_data

    save_data(data)
