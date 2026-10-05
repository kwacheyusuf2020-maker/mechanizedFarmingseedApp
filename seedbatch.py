class SeedBatch:
    def __init__(self, variety, quantity, quality_notes, production_date, harvest_date):
        self.variety = variety
        self.quantity = quantity
        self.quality_notes = quality_notes
        self.production_date = production_date
        self.harvest_date = harvest_date

    def display_details(self):
        print("Seed Variety:", self.variety)
        print("Quantity:", self.quantity)
        print("Quality Notes:", self.quality_notes)
        print("Production Date:", self.production_date)
        print("Harvest Date:", self.harvest_date)


# Create seed batches
seed1 = SeedBatch(
    "Maize",
    "100 kg",
    "Good quality, healthy seeds",
    "2026-02-10",
    "2026-09-20"
)

seed2 = SeedBatch(
    "Rice",
    "80 kg",
    "High quality seeds",
    "2026-05-15",
    "2026-09-25"
)

# production history
print("SEED PRODUCTION HISTORY")
print("----")

seed1.display_details()

print("\n===")

seed2.display_details()