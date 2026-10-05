class Crop:
    def __init__(self, name, growth_duration, soil_type, region):
        self.name = name
        self.growth_duration = growth_duration
        self.soil_type = soil_type
        self.region = region

    def display_info(self):
        print(f"Crop Name: {self.name}")
        print(f"Growth Duration: {self.growth_duration} days")
        print(f"Suitable Soil: {self.soil_type}")
        print(f"Region: {self.region}")