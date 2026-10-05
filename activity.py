
import json
import re
from datetime import datetime


def clean_text(text):

    return re.sub(r"\s+", " ", text).strip()


class ActivityLog:
    FILE_PATH = "activities.json"

    def __init__(self):
        self.activities = []

    def add_activity(self, activity_type, notes, date=None):
        entry = {
            "activity_type": activity_type,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "notes": clean_text(notes),
        }
        self.activities.append(entry)

    def save_data(self):
        try:
            with open(self.FILE_PATH, "w") as f:
                json.dump(self.activities, f, indent=4)
        except OSError as e:
            print(f"Could not save activity log: {e}")

    def load_data(self):
        try:
            with open(self.FILE_PATH, "r") as f:
                self.activities = json.load(f)
        except FileNotFoundError:
            self.activities = []
        except json.JSONDecodeError:
            print("Activity file is corrupted — starting with an empty log.")
            self.activities = []
