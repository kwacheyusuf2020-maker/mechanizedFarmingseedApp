import json
from pathlib import Path


DATA_FOLDER = Path(__file__).resolve().parent / "data"


def ensure_data_folder():
    DATA_FOLDER.mkdir(exist_ok=True)


def save_json(filename, data):
    try:
        ensure_data_folder()
        file_path = DATA_FOLDER / filename
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True, f"Data saved to {filename}."
    except (OSError, TypeError) as error:
        return False, f"Could not save data: {error}"


def load_json(filename, default=None):
    if default is None:
        default = []
    try:
        ensure_data_folder()
        file_path = DATA_FOLDER / filename
        if not file_path.exists():
            return default
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return default
