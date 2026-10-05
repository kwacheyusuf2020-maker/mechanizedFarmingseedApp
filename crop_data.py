class Crop:
    def __init__(self, name, crop_type, water_needs, soil_prefrence, temprature_range):
        self.name = name
        self.crop_type = crop_type
        self.water_needs = water_needs
        self.soil_prefrence = soil_prefrence
        self.temprature_range = temprature_range
        self.seed_varieties = []
