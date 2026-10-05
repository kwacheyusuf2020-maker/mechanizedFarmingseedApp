class EquipmentAdvisor:
    def __init__(self):
        self.equipment = {
            "ploughing": {
                "small": ["Hand Plough", "Mini Tiller"],
                "medium": ["Tractor Plough", "Disc Plough"],
                "large": ["Heavy-Duty Tractor", "Disc Plough"]
            },

            "planting": {
                "small": ["Hand Planter", "Seed Drill"],
                "medium": ["Tractor Planter", "Seed Drill"],
                "large": ["Precision Planter", "Tractor Planter"]
            },

            "harvesting": {
                "small": ["Manual Harvester", "Small Thresher"],
                "medium": ["Combine Harvester", "Mechanical Thresher"],
                "large": ["Large Combine Harvester", "Mechanical Thresher"]
            },

            "irrigation": {
                "small": ["Water Pump", "Drip Irrigation Kit"],
                "medium": ["Motorized Water Pump", "Sprinkler System"],
                "large": ["Large Irrigation Pump", "Center Pivot Irrigation"]
            },

            "weeding": {
                "small": ["Hoe", "Knapsack Sprayer"],
                "medium": ["Mechanical Weeder", "Boom Sprayer"],
                "large": ["Tractor Weeder", "Large Boom Sprayer"]
            }
        }

    def get_recommendation(self, activity, farm_size):
        """
        Recommend equipment based on farm activity and farm size.
        """

        activity = activity.lower().strip()
        farm_size = farm_size.lower().strip()

        if activity not in self.equipment:
            return {
                "success": False,
                "message": "Activity not found."
            }

        if farm_size not in ["small", "medium", "large"]:
            return {
                "success": False,
                "message": "Farm size must be small, medium, or large."
            }

        recommendations = self.equipment[activity][farm_size]

        return {
            "success": True,
            "activity": activity,
            "farm_size": farm_size,
            "equipment": recommendations
        }

    def display_recommendation(self, activity, farm_size):
        result = self.get_recommendation(activity, farm_size)

        if not result["success"]:
            print(result["message"])
            return

        print("\n===== EQUIPMENT ADVISOR =====")
        print(f"Farm Activity: {result['activity'].title()}")
        print(f"Farm Size: {result['farm_size'].title()}")

        print("\nRecommended Equipment:")

        for equipment in result["equipment"]:
            print(f"- {equipment}")


def main():
    advisor = EquipmentAdvisor()

    print("===== MECHANIZED FARMING EQUIPMENT ADVISOR =====")

    print("\nAvailable activities:")
    print("1. Ploughing")
    print("2. Planting")
    print("3. Harvesting")
    print("4. Irrigation")
    print("5. Weeding")

    activity = input("\nEnter farm activity: ")
    farm_size = input("Enter farm size (small/medium/large): ")

    advisor.display_recommendation(activity, farm_size)


if __name__ == "__main__":
    main()