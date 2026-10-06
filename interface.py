import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from validation import clean_text, validate_name, validate_region, validate_positive_number
from storage import save_json, load_json

from farm import Farm
from crop import Crop
from seed_batch import SeedBatch
from equipment_advisor import EquipmentAdvisor
from activity_log import ActivityLog
from gemini_advisor import get_ai_explanation

try:
    from quiz_generator import QuizGenerator
except ImportError:
    QuizGenerator = None


class MechanizedFarmingApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Mechanized Farming & Seed Production Advisor")
        self.geometry("1050x700")
        self.minsize(900, 600)

        self.activity_log = ActivityLog()
        self.equipment_advisor = EquipmentAdvisor()

        self.setup_style()
        self.create_header()
        self.create_notebook()

        self.create_dashboard_tab()
        self.create_farm_tab()
        self.create_crop_tab()
        self.create_seed_tab()
        self.create_equipment_tab()
        self.create_activity_tab()
        self.create_ai_tab()
        self.create_quiz_tab()

    def setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", 14, "bold"))

    def create_header(self):
        header = ttk.Frame(self, padding=15)
        header.pack(fill="x")
        ttk.Label(
            header,
            text="MECHANIZED FARMING & SEED PRODUCTION ADVISOR",
            style="Title.TLabel"
        ).pack()
        ttk.Label(
            header,
            text="Interface, Validation & Storage Module"
        ).pack(pady=(4, 0))

    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def add_row(self, parent, row, label, variable, combo_values=None):
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", padx=8, pady=8
        )
        if combo_values:
            widget = ttk.Combobox(
                parent, textvariable=variable,
                values=combo_values, state="readonly", width=38
            )
        else:
            widget = ttk.Entry(parent, textvariable=variable, width=40)
        widget.grid(row=row, column=1, sticky="w", padx=8, pady=8)
        return widget

    # ---------------- DASHBOARD ----------------

    def create_dashboard_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Dashboard")

        ttk.Label(tab, text="Welcome", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(
            tab,
            text=(
                "Use the tabs to manage farms, crops, seed batches, equipment, "
                "activities, AI advice and quiz records. Records are stored as JSON."
            ),
            justify="left"
        ).pack(anchor="w", pady=10)

        ttk.Button(
            tab, text="Refresh Dashboard",
            command=self.refresh_dashboard
        ).pack(anchor="w", pady=10)

        self.dashboard_status = ttk.Label(tab, text="")
        self.dashboard_status.pack(anchor="w", pady=10)
        self.refresh_dashboard()

    def refresh_dashboard(self):
        farms = load_json("farms.json", [])
        crops = load_json("crops.json", [])
        seeds = load_json("seed_batches.json", [])
        activities = load_json("activities.json", [])

        self.dashboard_status.config(
            text=(
                f"Saved records: Farms={len(farms)} | Crops={len(crops)} | "
                f"Seed batches={len(seeds)} | Activities={len(activities)}"
            )
        )

    # ---------------- FARM ----------------

    def create_farm_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Farm")

        self.farm_name = tk.StringVar()
        self.farm_size = tk.StringVar()
        self.farm_location = tk.StringVar()
        self.farm_soil = tk.StringVar()

        form = ttk.LabelFrame(tab, text="Farm Information", padding=15)
        form.pack(fill="x")

        self.add_row(form, 0, "Farm Name:", self.farm_name)
        self.add_row(form, 1, "Size (hectares):", self.farm_size)
        self.add_row(form, 2, "Location:", self.farm_location)
        self.add_row(form, 3, "Soil Type:", self.farm_soil)

        ttk.Button(form, text="Save Farm", command=self.save_farm).grid(
            row=4, column=1, sticky="w", padx=8, pady=15
        )

    def save_farm(self):
        valid, name = validate_name(self.farm_name.get())
        if not valid:
            messagebox.showerror("Validation Error", name)
            return

        valid, size = validate_positive_number(self.farm_size.get(), "Farm size")
        if not valid:
            messagebox.showerror("Validation Error", size)
            return

        valid, location = validate_region(self.farm_location.get())
        if not valid:
            messagebox.showerror("Validation Error", location)
            return

        soil = clean_text(self.farm_soil.get())
        if not soil:
            messagebox.showerror("Validation Error", "Soil type is required.")
            return

        farm = Farm(name, size, location, soil)

        records = load_json("farms.json", [])
        records.append({
            "name": farm.name,
            "size": farm.size,
            "location": farm.location,
            "soil_type": farm.soil_type
        })

        success, message = save_json("farms.json", records)
        if success:
            messagebox.showinfo("Success", "Farm saved successfully.")
            for v in (self.farm_name, self.farm_size, self.farm_location, self.farm_soil):
                v.set("")
            self.refresh_dashboard()
        else:
            messagebox.showerror("Storage Error", message)

    # ---------------- CROP ----------------

    def create_crop_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Crop")

        self.crop_name = tk.StringVar()
        self.crop_type = tk.StringVar()
        self.water_needs = tk.StringVar()
        self.soil_preference = tk.StringVar()
        self.temperature_range = tk.StringVar()

        form = ttk.LabelFrame(tab, text="Crop Information", padding=15)
        form.pack(fill="x")

        self.add_row(form, 0, "Crop Name:", self.crop_name)
        self.add_row(form, 1, "Crop Type:", self.crop_type)
        self.add_row(form, 2, "Water Needs:", self.water_needs)
        self.add_row(form, 3, "Soil Preference:", self.soil_preference)
        self.add_row(form, 4, "Temperature Range:", self.temperature_range)

        ttk.Button(form, text="Save Crop", command=self.save_crop).grid(
            row=5, column=1, sticky="w", padx=8, pady=15
        )

    def save_crop(self):
        valid, name = validate_name(self.crop_name.get())
        if not valid:
            messagebox.showerror("Validation Error", name)
            return

        crop_type = clean_text(self.crop_type.get())
        water = clean_text(self.water_needs.get())
        soil = clean_text(self.soil_preference.get())
        temperature = clean_text(self.temperature_range.get())

        if not all((crop_type, water, soil, temperature)):
            messagebox.showerror("Validation Error", "Complete all crop fields.")
            return

        crop = Crop(name, crop_type, water, soil, temperature)

        records = load_json("crops.json", [])
        records.append({
            "name": crop.name,
            "crop_type": crop.crop_type,
            "water_needs": crop.water_needs,
            "soil_prefrence": crop.soil_prefrence,
            "temprature_range": crop.temprature_range,
            "seed_varieties": crop.seed_varieties
        })

        success, message = save_json("crops.json", records)
        if success:
            messagebox.showinfo("Success", "Crop saved successfully.")
            for v in (
                self.crop_name, self.crop_type, self.water_needs,
                self.soil_preference, self.temperature_range
            ):
                v.set("")
            self.refresh_dashboard()
        else:
            messagebox.showerror("Storage Error", message)

    # ---------------- SEED BATCH ----------------

    def create_seed_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Seed Batch")

        self.seed_variety = tk.StringVar()
        self.seed_quantity = tk.StringVar()
        self.seed_quality = tk.StringVar()
        self.seed_production_date = tk.StringVar()
        self.seed_harvest_date = tk.StringVar()

        form = ttk.LabelFrame(tab, text="Seed Batch Information", padding=15)
        form.pack(fill="x")

        self.add_row(form, 0, "Variety:", self.seed_variety)
        self.add_row(form, 1, "Quantity:", self.seed_quantity)
        self.add_row(form, 2, "Quality Notes:", self.seed_quality)
        self.add_row(form, 3, "Production Date (YYYY-MM-DD):", self.seed_production_date)
        self.add_row(form, 4, "Harvest Date (YYYY-MM-DD):", self.seed_harvest_date)

        ttk.Button(form, text="Save Seed Batch", command=self.save_seed_batch).grid(
            row=5, column=1, sticky="w", padx=8, pady=15
        )

    def valid_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def save_seed_batch(self):
        values = [
            clean_text(self.seed_variety.get()),
            clean_text(self.seed_quantity.get()),
            clean_text(self.seed_quality.get()),
            clean_text(self.seed_production_date.get()),
            clean_text(self.seed_harvest_date.get())
        ]

        if not all(values):
            messagebox.showerror("Validation Error", "Complete all seed batch fields.")
            return

        variety, quantity, quality, production, harvest = values

        if not self.valid_date(production) or not self.valid_date(harvest):
            messagebox.showerror("Validation Error", "Dates must use YYYY-MM-DD.")
            return

        seed = SeedBatch(variety, quantity, quality, production, harvest)

        records = load_json("seed_batches.json", [])
        records.append({
            "variety": seed.variety,
            "quantity": seed.quantity,
            "quality_notes": seed.quality_notes,
            "production_date": seed.production_date,
            "harvest_date": seed.harvest_date
        })

        success, message = save_json("seed_batches.json", records)
        if success:
            messagebox.showinfo("Success", "Seed batch saved successfully.")
            for v in (
                self.seed_variety, self.seed_quantity, self.seed_quality,
                self.seed_production_date, self.seed_harvest_date
            ):
                v.set("")
            self.refresh_dashboard()
        else:
            messagebox.showerror("Storage Error", message)

    # ---------------- EQUIPMENT ----------------

    def create_equipment_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Equipment")

        self.equipment_activity = tk.StringVar(value="ploughing")
        self.equipment_size = tk.StringVar(value="small")

        form = ttk.LabelFrame(tab, text="Equipment Advisor", padding=15)
        form.pack(fill="x")

        self.add_row(
            form, 0, "Farm Activity:", self.equipment_activity,
            ["ploughing", "planting", "harvesting", "irrigation", "weeding"]
        )
        self.add_row(
            form, 1, "Farm Size:", self.equipment_size,
            ["small", "medium", "large"]
        )

        ttk.Button(
            form, text="Get Recommendation",
            command=self.get_equipment_recommendation
        ).grid(row=2, column=1, sticky="w", padx=8, pady=15)

        self.equipment_output = tk.Text(tab, height=12, wrap="word")
        self.equipment_output.pack(fill="both", expand=True, pady=15)

    def get_equipment_recommendation(self):
        result = self.equipment_advisor.get_recommendation(
            self.equipment_activity.get(),
            self.equipment_size.get()
        )

        self.equipment_output.delete("1.0", tk.END)

        if not result.get("success"):
            self.equipment_output.insert(tk.END, result.get("message", "No recommendation."))
            return

        self.equipment_output.insert(
            tk.END,
            f"Activity: {result['activity'].title()}\n"
            f"Farm Size: {result['farm_size'].title()}\n\n"
            "Recommended Equipment:\n"
        )
        for item in result["equipment"]:
            self.equipment_output.insert(tk.END, f"• {item}\n")

    # ---------------- ACTIVITY LOG ----------------

    def create_activity_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Activity Log")

        self.activity_type = tk.StringVar()
        self.activity_date = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )

        form = ttk.LabelFrame(tab, text="Farm Activity", padding=15)
        form.pack(fill="x")

        self.add_row(form, 0, "Activity Type:", self.activity_type)
        self.add_row(form, 1, "Date (YYYY-MM-DD):", self.activity_date)

        ttk.Label(form, text="Notes:").grid(
            row=2, column=0, sticky="nw", padx=8, pady=8
        )

        self.activity_notes = tk.Text(form, height=5, width=50)
        self.activity_notes.grid(row=2, column=1, padx=8, pady=8)

        ttk.Button(
            form, text="Save Activity",
            command=self.save_activity
        ).grid(row=3, column=1, sticky="w", padx=8, pady=15)

    def save_activity(self):
        activity_type = clean_text(self.activity_type.get())
        date = clean_text(self.activity_date.get())
        notes = clean_text(self.activity_notes.get("1.0", tk.END))

        if not all((activity_type, date, notes)):
            messagebox.showerror("Validation Error", "Complete all activity fields.")
            return

        if not self.valid_date(date):
            messagebox.showerror("Validation Error", "Date must use YYYY-MM-DD.")
            return

        self.activity_log.add_activity(activity_type, notes, date)
        success, message = save_json(
            "activities.json", self.activity_log.activities
        )

        if success:
            messagebox.showinfo("Success", "Activity saved successfully.")
            self.activity_type.set("")
            self.activity_date.set(datetime.now().strftime("%Y-%m-%d"))
            self.activity_notes.delete("1.0", tk.END)
            self.refresh_dashboard()
        else:
            messagebox.showerror("Storage Error", message)

    # ---------------- AI ADVISOR ----------------

    def create_ai_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="AI Advisor")

        self.ai_crop = tk.StringVar()
        self.ai_farm_size = tk.StringVar()
        self.ai_soil = tk.StringVar()

        form = ttk.LabelFrame(tab, text="Gemini Farming Advisor", padding=15)
        form.pack(fill="x")

        self.add_row(form, 0, "Crop Name:", self.ai_crop)
        self.add_row(form, 1, "Farm Size (hectares):", self.ai_farm_size)
        self.add_row(form, 2, "Soil Type:", self.ai_soil)

        ttk.Button(
            form, text="Get AI Advice",
            command=self.get_ai_advice
        ).grid(row=3, column=1, sticky="w", padx=8, pady=15)

        self.ai_output = tk.Text(tab, height=18, wrap="word")
        self.ai_output.pack(fill="both", expand=True, pady=15)

    def get_ai_advice(self):
        crop = clean_text(self.ai_crop.get())
        soil = clean_text(self.ai_soil.get())

        valid, farm_size = validate_positive_number(
            self.ai_farm_size.get(), "Farm size"
        )

        if not crop or not soil:
            messagebox.showerror("Validation Error", "Crop and soil are required.")
            return

        if not valid:
            messagebox.showerror("Validation Error", farm_size)
            return

        try:
            advice = get_ai_explanation(crop, farm_size, soil)
        except Exception as error:
            advice = f"AI explanation unavailable: {error}"

        self.ai_output.delete("1.0", tk.END)
        self.ai_output.insert(tk.END, advice)

    # ---------------- QUIZ ----------------

    def create_quiz_tab(self):
        tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(tab, text="Quiz")

        ttk.Label(tab, text="Quiz Generator", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(
            tab,
            text=(
                "The existing Quiz Generator remains unchanged. "
                "This tab can display its saved score history."
            ),
            wraplength=800
        ).pack(anchor="w", pady=10)

        ttk.Button(
            tab, text="Show Saved Quiz Scores",
            command=self.show_quiz_scores
        ).pack(anchor="w", pady=10)

        self.quiz_output = tk.Text(tab, height=18, wrap="word")
        self.quiz_output.pack(fill="both", expand=True)

    def show_quiz_scores(self):
        self.quiz_output.delete("1.0", tk.END)

        if QuizGenerator is None:
            self.quiz_output.insert(
                tk.END,
                "QuizGenerator could not be imported. Check quiz_generator.py."
            )
            return

        try:
            quiz = QuizGenerator()
            history = quiz.get_score_history()

            if not history:
                self.quiz_output.insert(tk.END, "No saved quiz scores yet.")
                return

            for record in history:
                self.quiz_output.insert(tk.END, f"{record}\n\n")

        except Exception as error:
            self.quiz_output.insert(tk.END, f"Could not load quiz scores.\nError: {error}")


if __name__ == "__main__":
    app = MechanizedFarmingApp()
    app.mainloop()
