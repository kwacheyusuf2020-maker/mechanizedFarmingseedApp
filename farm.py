class Farm:

    def __init__(self, name, size, location, soil_type, owner=""):
        self.name = self._check_text(name, "Farm name")
        self.size = self._check_size(size)
        self.location = self._check_text(location, "Location")
        self.soil_type = self._check_text(soil_type, "Soil type")
        self.owner = str(owner).strip()

    @staticmethod
    def _check_text(value, field_name):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        return value

    @staticmethod
    def _check_size(size):
        try:
            size = float(size)
        except (TypeError, ValueError) as error:
            raise ValueError("Farm size must be a number.") from error

        if size <= 0:
            raise ValueError("Farm size must be greater than zero.")
        return size

    def display_info(self):
        print(f"Farm Name: {self.name}")
        print(f"Size: {self.size} hectares")
        print(f"Location: {self.location}")
        print(f"Soil Type: {self.soil_type}")
        if self.owner:
            print(f"Owner: {self.owner}")

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "location": self.location,
            "soil_type": self.soil_type,
            "owner": self.owner,
        }
