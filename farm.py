class Farm:
    def __init__(self, name, size, location, soil_type):
        self.name = name
        self.size = size
        self.location = location
        self.soil_type = soil_type

    def display_info(self):
        print(f"Farm Name: {self.name}")
        print(f"Size: {self.size} hectares")
        print(f"Location: {self.location}")
        print(f"Soil Type: {self.soil_type}")


# Get real details from whoever is testing it
name = input("Enter farm name: ")
size = float(input("Enter farm size (hectares): "))
location = input("Enter location: ")
soil_type = input("Enter soil type: ")

farm1 = Farm(name, size, location, soil_type)
farm1.display_info()