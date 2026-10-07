class Crop:

    def __init__(self, name, crop_type, water_needs, soil_preference, temperature_range):
        self.name = self._check_text(name, "Crop name")
        self.crop_type = self._check_text(crop_type, "Crop type")
        self.water_needs = self._check_text(water_needs, "Water needs")
        self.soil_preference = self._check_text(soil_preference, "Soil preference")
        self.temperature_range = self._check_text(temperature_range, "Temperature range")
        self.seed_varieties = []

        self.soil_prefrence = self.soil_preference
        self.temprature_range = self.temperature_range

    @staticmethod
    def _check_text(value, field_name):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        return value

    def add_seed_variety(self, variety):
        variety = self._check_text(variety, "Seed variety")
        if variety not in self.seed_varieties:
            self.seed_varieties.append(variety)

    def display_info(self):
        print(f"Crop Name: {self.name}")
        print(f"Crop Type: {self.crop_type}")
        print(f"Water Needs: {self.water_needs}")
        print(f"Soil Preference: {self.soil_preference}")
        print(f"Temperature Range: {self.temperature_range}")
        print("Seed Varieties:", ", ".join(self.seed_varieties) or "None added")

    def to_dict(self):
        return {
            "name": self.name,
            "crop_type": self.crop_type,
            "water_needs": self.water_needs,
            "soil_preference": self.soil_preference,
            "temperature_range": self.temperature_range,
            "seed_varieties": self.seed_varieties,
        }
