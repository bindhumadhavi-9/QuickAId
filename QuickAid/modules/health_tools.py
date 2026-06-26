"""
Health Tools Module
Health calculators: BMI Calculator, Water Intake Calculator, Calorie Estimator
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card
import math


class HealthToolsPage(ctk.CTkFrame):
    """Health Tools page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_tools()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Health Tools",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Use our health calculators to monitor your wellness",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_tools(self):
        """Create health tools"""
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_columnconfigure((0, 1), weight=1)

        # BMI Calculator
        self.create_bmi_tool(container)

        # Water Intake Calculator
        self.create_water_tool(container)

        # Calorie Estimator
        self.create_calorie_tool(container)

    def create_bmi_tool(self, parent):
        """Create BMI Calculator"""
        card = create_card(parent)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            frame,
            text="BMI Calculator",
            font=ctk.CTkFont(size=18, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 20))

        # Weight
        weight_label = ctk.CTkLabel(
            frame,
            text="Weight (kg):",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        weight_label.pack(anchor="w", pady=(0, 5))

        weight_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter weight in kg",
            height=35,
            corner_radius=8
        )
        weight_entry.pack(fill="x", pady=(0, 15))

        # Height
        height_label = ctk.CTkLabel(
            frame,
            text="Height (cm):",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        height_label.pack(anchor="w", pady=(0, 5))

        height_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter height in cm",
            height=35,
            corner_radius=8
        )
        height_entry.pack(fill="x", pady=(0, 20))

        # Result frame
        self.bmi_result_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.bmi_result_frame.pack(fill="x")

        # Calculate button
        def calculate_bmi():
            try:
                weight = float(weight_entry.get())
                height = float(height_entry.get()) / 100  # Convert cm to m

                if weight > 0 and height > 0:
                    bmi = weight / (height ** 2)
                    self.show_bmi_result(bmi)
            except ValueError:
                pass

        calc_btn = ctk.CTkButton(
            frame,
            text="Calculate BMI",
            command=calculate_bmi,
            fg_color=self.colors["success"],
            hover_color="#059669",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        calc_btn.pack(fill="x", pady=(20, 0))

    def show_bmi_result(self, bmi):
        """Show BMI result"""
        # Clear previous result
        for widget in self.bmi_result_frame.winfo_children():
            widget.destroy()

        # Determine category
        if bmi < 18.5:
            category = "Underweight"
            color = self.colors["info"]
            advice = "You may need to gain weight. Consult a nutritionist."
        elif bmi < 25:
            category = "Normal Weight"
            color = self.colors["success"]
            advice = "Keep up the healthy lifestyle!"
        elif bmi < 30:
            category = "Overweight"
            color = self.colors["warning"]
            advice = "Consider increasing exercise and healthy diet."
        else:
            category = "Obese"
            color = self.colors["danger"]
            advice = "Please consult a healthcare provider."

        result_label = ctk.CTkLabel(
            self.bmi_result_frame,
            text=f"BMI: {bmi:.1f}",
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=color
        )
        result_label.pack(pady=(20, 5))

        category_label = ctk.CTkLabel(
            self.bmi_result_frame,
            text=category,
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=color
        )
        category_label.pack(pady=(0, 10))

        advice_label = ctk.CTkLabel(
            self.bmi_result_frame,
            text=advice,
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="center",
            wraplength=250
        )
        advice_label.pack(pady=(0, 10))

    def create_water_tool(self, parent):
        """Create Water Intake Calculator"""
        card = create_card(parent)
        card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            frame,
            text="Water Intake Calculator",
            font=ctk.CTkFont(size=18, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 20))

        # Body weight
        weight_label = ctk.CTkLabel(
            frame,
            text="Body Weight (kg):",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        weight_label.pack(anchor="w", pady=(0, 5))

        weight_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter weight in kg",
            height=35,
            corner_radius=8
        )
        weight_entry.pack(fill="x", pady=(0, 15))

        # Activity level
        activity_label = ctk.CTkLabel(
            frame,
            text="Activity Level:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        activity_label.pack(anchor="w", pady=(0, 5))

        activity_var = ctk.StringVar(value="Moderate")
        activity_combo = ctk.CTkComboBox(
            frame,
            values=["Sedentary", "Light", "Moderate", "Active", "Very Active"],
            variable=activity_var,
            state="readonly",
            height=35,
            corner_radius=8
        )
        activity_combo.pack(fill="x", pady=(0, 20))

        # Result frame
        self.water_result_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.water_result_frame.pack(fill="x")

        # Calculate button
        def calculate_water():
            try:
                weight = float(weight_entry.get())
                activity = activity_var.get()

                if weight > 0:
                    # Base calculation: 30-35 ml per kg
                    base_water = weight * 30

                    # Activity multiplier
                    multipliers = {
                        "Sedentary": 1.0,
                        "Light": 1.1,
                        "Moderate": 1.25,
                        "Active": 1.5,
                        "Very Active": 1.75
                    }
                    water_intake = base_water * multipliers.get(activity, 1.0)
                    self.show_water_result(water_intake)
            except ValueError:
                pass

        calc_btn = ctk.CTkButton(
            frame,
            text="Calculate Intake",
            command=calculate_water,
            fg_color=self.colors["info"],
            hover_color="#0284c7",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        calc_btn.pack(fill="x", pady=(20, 0))

    def show_water_result(self, liters):
        """Show water intake result"""
        # Clear previous result
        for widget in self.water_result_frame.winfo_children():
            widget.destroy()

        glasses = liters / 0.25  # 250ml per glass

        result_label = ctk.CTkLabel(
            self.water_result_frame,
            text=f"{liters:.1f} L per day",
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=self.colors["info"]
        )
        result_label.pack(pady=(20, 5))

        glasses_label = ctk.CTkLabel(
            self.water_result_frame,
            text=f"Approximately {glasses:.0f} glasses (250ml each)",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        glasses_label.pack(pady=(0, 10))

        advice_label = ctk.CTkLabel(
            self.water_result_frame,
            text="Spread water intake throughout the day.\nDrink more in hot weather or during exercise.",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="center",
            wraplength=250
        )
        advice_label.pack(pady=(0, 10))

    def create_calorie_tool(self, parent):
        """Create Calorie Estimator"""
        card = create_card(parent)
        card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            frame,
            text="Daily Calorie Estimator",
            font=ctk.CTkFont(size=18, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 20))

        # Input frame
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 20))
        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Age
        age_label = ctk.CTkLabel(
            input_frame,
            text="Age:",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        age_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))

        age_entry = ctk.CTkEntry(input_frame, placeholder_text="years", height=30, width=60)
        age_entry.grid(row=0, column=0, sticky="e", padx=(0, 10))

        # Weight
        weight_label = ctk.CTkLabel(
            input_frame,
            text="Weight (kg):",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        weight_label.grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 5))

        weight_entry = ctk.CTkEntry(input_frame, placeholder_text="kg", height=30, width=60)
        weight_entry.grid(row=0, column=1, sticky="e", padx=(0, 10))

        # Height
        height_label = ctk.CTkLabel(
            input_frame,
            text="Height (cm):",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        height_label.grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 5))

        height_entry = ctk.CTkEntry(input_frame, placeholder_text="cm", height=30, width=60)
        height_entry.grid(row=0, column=2, sticky="e", padx=(0, 10))

        # Gender
        gender_label = ctk.CTkLabel(
            input_frame,
            text="Gender:",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        gender_label.grid(row=0, column=3, sticky="w", padx=(0, 5), pady=(0, 5))

        gender_var = ctk.StringVar(value="Male")
        gender_combo = ctk.CTkComboBox(
            input_frame,
            values=["Male", "Female"],
            variable=gender_var,
            state="readonly",
            height=30,
            width=70
        )
        gender_combo.grid(row=0, column=3, sticky="e")

        # Activity level
        activity_label = ctk.CTkLabel(
            frame,
            text="Activity Level:",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        activity_label.pack(anchor="w", pady=(0, 5))

        activity_var = ctk.StringVar(value="Moderate")
        activity_combo = ctk.CTkComboBox(
            frame,
            values=["Sedentary", "Light", "Moderate", "Active", "Very Active"],
            variable=activity_var,
            state="readonly",
            height=35,
            corner_radius=8
        )
        activity_combo.pack(fill="x", pady=(0, 20))

        # Result frame
        self.calorie_result_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.calorie_result_frame.pack(fill="x")

        # Calculate button
        def calculate_calories():
            try:
                age = int(age_entry.get())
                weight = float(weight_entry.get())
                height = float(height_entry.get())
                gender = gender_var.get()
                activity = activity_var.get()

                if age > 0 and weight > 0 and height > 0:
                    # Harris-Benedict equation
                    if gender == "Male":
                        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
                    else:
                        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

                    # Activity multiplier
                    multipliers = {
                        "Sedentary": 1.2,
                        "Light": 1.375,
                        "Moderate": 1.55,
                        "Active": 1.725,
                        "Very Active": 1.9
                    }
                    tdee = bmr * multipliers.get(activity, 1.55)
                    self.show_calorie_result(tdee)
            except ValueError:
                pass

        calc_btn = ctk.CTkButton(
            frame,
            text="Calculate Daily Calories",
            command=calculate_calories,
            fg_color=self.colors["warning"],
            hover_color="#d97706",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        calc_btn.pack(fill="x", pady=(20, 0))

    def show_calorie_result(self, calories):
        """Show calorie result"""
        # Clear previous result
        for widget in self.calorie_result_frame.winfo_children():
            widget.destroy()

        result_label = ctk.CTkLabel(
            self.calorie_result_frame,
            text=f"{calories:.0f} calories per day",
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=self.colors["warning"]
        )
        result_label.pack(pady=(20, 5))

        advice_label = ctk.CTkLabel(
            self.calorie_result_frame,
            text=f"To maintain weight: {calories:.0f} kcal/day\nTo lose weight: {calories * 0.8:.0f} kcal/day\nTo gain weight: {calories * 1.2:.0f} kcal/day",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="center",
            wraplength=400
        )
        advice_label.pack(pady=(0, 10))
