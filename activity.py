import json
import re
from datetime import datetime


def clean_text(text):
    return re.sub(r"\s+", " ", str(text)).strip()


class ActivityLog:

    VALID_ACTIVITY_TYPES = ("planting", "fertilizing", "harvesting")

    def __init__(self, file_path="activities.json"):
        self.file_path = file_path
        self.activities = []

    def add_activity(self, activity_type, notes, date=None, farm_name=None, crop_name=None):
        activity_type = clean_text(activity_type).lower()
        notes = clean_text(notes)

        if activity_type not in self.VALID_ACTIVITY_TYPES:
            allowed = ", ".join(self.VALID_ACTIVITY_TYPES)
            raise ValueError(f"Activity type must be one of: {allowed}.")

        if not notes:
            raise ValueError("Notes cannot be empty.")

        activity_date = date or datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(activity_date, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError("Date must be written as YYYY-MM-DD.") from error

        activity = {
            "activity_type": activity_type,
            "date": activity_date,
            "notes": notes,
            "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        if farm_name:
            activity["farm_name"] = clean_text(farm_name)
        if crop_name:
            activity["crop_name"] = clean_text(crop_name)

        self.activities.append(activity)
        return activity

    def get_activities(self, activity_type=None):
        if activity_type is None:
            return self.activities.copy()

        activity_type = clean_text(activity_type).lower()
        return [
            activity
            for activity in self.activities
            if activity["activity_type"] == activity_type
        ]

    def display_activities(self, activity_type=None):
        activities = self.get_activities(activity_type)

        if not activities:
            print("No activities found.")
            return

        for number, activity in enumerate(activities, start=1):
            print(f"\nActivity {number}")
            print(f"Type: {activity['activity_type'].title()}")
            print(f"Date: {activity['date']}")
            print(f"Notes: {activity['notes']}")
            if activity.get("farm_name"):
                print(f"Farm: {activity['farm_name']}")
            if activity.get("crop_name"):
                print(f"Crop: {activity['crop_name']}")
            print(f"Recorded at: {activity['recorded_at']}")

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.activities, file, indent=4)
            print("Activity log saved successfully.")
        except OSError as error:
            print(f"Could not save activity log: {error}")

    def load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                loaded_activities = json.load(file)

            if isinstance(loaded_activities, list):
                self.activities = loaded_activities
            else:
                print("Activity file has an invalid format. Starting with an empty log.")
                self.activities = []
        except FileNotFoundError:
            self.activities = []
        except (OSError, json.JSONDecodeError) as error:
            print(f"Could not load activity log: {error}")
            self.activities = []


def main():
    log = ActivityLog()
    log.load_data()

    print("Farm Activity Log")
    print("Activity types: planting, fertilizing, harvesting")

    try:
        activity_type = input("Enter activity type: ")
        notes = input("Enter activity notes: ")
        date = input("Enter date (YYYY-MM-DD), or press Enter for today: ")
        farm_name = input("Enter farm name (optional): ")
        crop_name = input("Enter crop name (optional): ")

        log.add_activity(
            activity_type,
            notes,
            date or None,
            farm_name or None,
            crop_name or None,
        )
        log.save_data()
        log.display_activities()
    except ValueError as error:
        print(f"Could not add activity: {error}")


if __name__ == "__main__":
    main()
