from pathlib import Path

from activity import ActivityLog
from crop import Crop
from farm import Farm


def get_required_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def create_farm():
    print("\nCreate Farm")
    try:
        return Farm(
            get_required_input("Farm name: "),
            get_required_input("Farm size in hectares: "),
            get_required_input("Location or region: "),
            get_required_input("Soil type: "),
            input("Owner name (optional): ").strip(),
        )
    except ValueError as error:
        print(f"Could not create farm: {error}")
        return None


def create_crop():
    print("\nCreate Crop")
    try:
        crop = Crop(
            get_required_input("Crop name: "),
            get_required_input("Crop type: "),
            get_required_input("Water needs: "),
            get_required_input("Preferred soil type: "),
            get_required_input("Temperature range: "),
        )

        variety = input("Seed variety (optional): ").strip()
        if variety:
            crop.add_seed_variety(variety)
        return crop
    except ValueError as error:
        print(f"Could not create crop: {error}")
        return None


def record_activity(activity_log, farm, crop):
    if farm is None or crop is None:
        print("Create both a farm and a crop before recording an activity.")
        return

    print("\nRecord Activity")
    print("Choose: planting, fertilizing, or harvesting")
    try:
        activity_log.add_activity(
            get_required_input("Activity type: "),
            get_required_input("Notes: "),
            input("Date (YYYY-MM-DD, press Enter for today): ").strip() or None,
            farm.name,
            crop.name,
        )
        activity_log.save_data()
    except ValueError as error:
        print(f"Could not record activity: {error}")


def show_current_details(farm, crop):
    print("\nCurrent Details")
    if farm is None:
        print("No farm has been created yet.")
    else:
        farm.display_info()

    print()
    if crop is None:
        print("No crop has been created yet.")
    else:
        crop.display_info()


def show_menu():
    print("\nMechanized Farming and Seed Production Advisor")
    print("1. Create or replace farm")
    print("2. Create or replace crop")
    print("3. Record activity")
    print("4. View activity history")
    print("5. View current farm and crop")
    print("6. Exit")


def main():
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    activity_log = ActivityLog(data_folder / "activities.json")
    activity_log.load_data()
    current_farm = None
    current_crop = None

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            new_farm = create_farm()
            if new_farm:
                current_farm = new_farm
                print("Farm created successfully.")
        elif choice == "2":
            new_crop = create_crop()
            if new_crop:
                current_crop = new_crop
                print("Crop created successfully.")
        elif choice == "3":
            record_activity(activity_log, current_farm, current_crop)
        elif choice == "4":
            activity_log.display_activities()
        elif choice == "5":
            show_current_details(current_farm, current_crop)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
