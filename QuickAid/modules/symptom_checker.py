"""
Symptom Checker Module
Rule-based symptom checker with symptom selection, possible conditions display, and health recommendations
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card
import json


class SymptomCheckerPage(ctk.CTkFrame):
    """Symptom Checker page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.selected_symptoms = []

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_main_content()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=100)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Symptom Checker",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Select your symptoms to identify possible conditions",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_main_content(self):
        """Create main content area with symptoms and results"""
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure((0, 1), weight=1)

        # Left column - Symptoms
        left_frame = create_card(main_container)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        left_frame.grid_rowconfigure(1, weight=1)

        symptoms_title = ctk.CTkLabel(
            left_frame,
            text="Select Your Symptoms",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        symptoms_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Symptoms list frame
        symptoms_container = ctk.CTkScrollableFrame(
            left_frame,
            fg_color="transparent"
        )
        symptoms_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        symptoms = [
            "Fever", "Cough", "Sore Throat", "Headache", "Body Aches",
            "Fatigue", "Shortness of Breath", "Chest Pain", "Nausea", "Vomiting",
            "Diarrhea", "Constipation", "Abdominal Pain", "Dizziness", "Rash",
            "Itching", "Swelling", "Joint Pain", "Muscle Pain", "Weakness",
            "Chills", "Loss of Appetite", "Sweating", "Dry Mouth", "Red Eyes"
        ]

        self.symptom_vars = {}
        for symptom in symptoms:
            var = ctk.StringVar(value="off")
            self.symptom_vars[symptom] = var

            checkbox_frame = ctk.CTkFrame(symptoms_container, fg_color="transparent")
            checkbox_frame.pack(fill="x", pady=8)

            checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text=symptom,
                variable=var,
                onvalue="on",
                offvalue="off",
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                text_color=self.colors["text_primary"],
                checkbox_width=20,
                checkbox_height=20,
                command=self.on_symptom_changed
            )
            checkbox.pack(side="left", fill="x", expand=True)

        # Clear button
        clear_btn = ctk.CTkButton(
            left_frame,
            text="Clear All",
            command=self.clear_symptoms,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_secondary"],
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            height=35,
            corner_radius=8
        )
        clear_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))

        # Right column - Results
        right_frame = create_card(main_container)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        right_frame.grid_rowconfigure(1, weight=1)

        results_title = ctk.CTkLabel(
            right_frame,
            text="Possible Conditions",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        results_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Results container
        self.results_container = ctk.CTkScrollableFrame(
            right_frame,
            fg_color="transparent"
        )
        self.results_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Placeholder
        self.placeholder = ctk.CTkLabel(
            self.results_container,
            text="Select symptoms to see possible conditions",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        self.placeholder.pack(pady=20)

        # Recommendations section
        recommendations_frame = create_card(main_container)
        recommendations_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        rec_title = ctk.CTkLabel(
            recommendations_frame,
            text="Health Recommendations",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        rec_title.pack(anchor="w", padx=20, pady=(20, 10))

        self.recommendations_label = ctk.CTkLabel(
            recommendations_frame,
            text="Your personalized recommendations will appear here",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=600
        )
        self.recommendations_label.pack(anchor="w", padx=20, pady=(0, 20))

    def on_symptom_changed(self):
        """Handle symptom selection changes"""
        self.selected_symptoms = [
            symptom for symptom, var in self.symptom_vars.items()
            if var.get() == "on"
        ]
        self.update_results()

    def update_results(self):
        """Update possible conditions based on selected symptoms"""
        # Clear placeholder
        self.placeholder.pack_forget()

        # Clear existing results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        if not self.selected_symptoms:
            self.placeholder.pack(pady=20)
            self.recommendations_label.configure(
                text="Your personalized recommendations will appear here"
            )
            return

        # Symptom to condition mapping
        symptom_conditions = {
            "Fever": ["Cold/Flu", "COVID-19", "Malaria", "Typhoid", "Infection"],
            "Cough": ["Cold/Flu", "COVID-19", "Bronchitis", "Pneumonia", "Asthma"],
            "Sore Throat": ["Cold/Flu", "COVID-19", "Strep Throat", "Pharyngitis"],
            "Headache": ["Migraine", "Tension Headache", "Cold/Flu", "Dehydration"],
            "Body Aches": ["Cold/Flu", "COVID-19", "Arthritis", "Fibromyalgia"],
            "Fatigue": ["Anemia", "Thyroid Issues", "Depression", "Chronic Fatigue"],
            "Shortness of Breath": ["Asthma", "Pneumonia", "Heart Disease", "Anxiety"],
            "Chest Pain": ["Heart Disease", "Anxiety", "Gastritis", "Muscle Strain"],
            "Nausea": ["Gastroenteritis", "Migraine", "Pregnancy", "Food Poisoning"],
            "Vomiting": ["Gastroenteritis", "Food Poisoning", "Appendicitis"],
            "Diarrhea": ["Gastroenteritis", "Food Poisoning", "IBS", "Cholera"],
            "Constipation": ["IBS", "Dehydration", "Hemorrhoids", "Poor Diet"],
            "Abdominal Pain": ["Gastritis", "Appendicitis", "Ulcer", "IBS"],
            "Dizziness": ["Vertigo", "Low Blood Pressure", "Anxiety", "Inner Ear Issue"],
            "Rash": ["Chickenpox", "Measles", "Dermatitis", "Allergic Reaction"],
            "Itching": ["Allergies", "Dermatitis", "Dry Skin", "Fungal Infection"],
            "Swelling": ["Inflammation", "Allergy", "Lymphadenopathy", "Injury"],
            "Joint Pain": ["Arthritis", "Gout", "Lupus", "Rheumatoid Arthritis"],
            "Muscle Pain": ["Myositis", "Muscle Strain", "Fibromyalgia", "Exercise"],
            "Weakness": ["Anemia", "Thyroid Issues", "Malnutrition", "Depression"],
            "Chills": ["Fever", "Infection", "Cold/Flu", "Malaria"],
            "Loss of Appetite": ["Depression", "Infection", "Cancer", "Liver Disease"],
            "Sweating": ["Fever", "Anxiety", "Hyperthyroidism", "Menopause"],
            "Dry Mouth": ["Dehydration", "Diabetes", "Thyroid Issues", "Sjögren's"],
            "Red Eyes": ["Conjunctivitis", "Allergy", "Eye Strain", "Uveitis"]
        }

        # Collect all conditions from selected symptoms
        conditions_count = {}
        for symptom in self.selected_symptoms:
            conditions = symptom_conditions.get(symptom, [])
            for condition in conditions:
                conditions_count[condition] = conditions_count.get(condition, 0) + 1

        # Sort by frequency
        sorted_conditions = sorted(
            conditions_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Display conditions
        for condition, count in sorted_conditions[:8]:
            self.display_condition_card(condition, count)

        # Update recommendations
        self.update_recommendations()

    def display_condition_card(self, condition, frequency):
        """Display a condition card"""
        card = create_card(self.results_container)
        card.pack(fill="x", pady=8)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=15)

        # Condition name and frequency
        name_frame = ctk.CTkFrame(frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 5))

        name_label = ctk.CTkLabel(
            name_frame,
            text=condition,
            font=ctk.CTkFont(size=13, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name_label.pack(side="left", anchor="w")

        # Frequency bar
        freq_label = ctk.CTkLabel(
            name_frame,
            text=f"{int(frequency)} match" + ("es" if frequency > 1 else ""),
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        freq_label.pack(side="right")

        # Progress bar
        progress = ctk.CTkProgressBar(
            frame,
            value=frequency / len(self.selected_symptoms),
            height=4,
            fg_color=self.colors["bg_tertiary"],
            progress_color=self.colors["accent"]
        )
        progress.pack(fill="x", pady=(5, 0))

    def clear_symptoms(self):
        """Clear all selected symptoms"""
        for var in self.symptom_vars.values():
            var.set("off")
        self.selected_symptoms = []
        self.update_results()

    def update_recommendations(self):
        """Update health recommendations"""
        if not self.selected_symptoms:
            return

        recommendations = []

        # General recommendations based on symptoms
        if any(s in self.selected_symptoms for s in ["Fever", "Cough", "Sore Throat", "Body Aches"]):
            recommendations.append("• Rest and get adequate sleep (7-9 hours)")
            recommendations.append("• Stay hydrated - drink plenty of water")
            recommendations.append("• Gargle with warm salt water for sore throat")

        if any(s in self.selected_symptoms for s in ["Nausea", "Vomiting", "Diarrhea"]):
            recommendations.append("• Avoid solid foods; eat bland, easily digestible foods")
            recommendations.append("• Drink oral rehydration solution (ORS)")
            recommendations.append("• Avoid dairy and fatty foods")

        if any(s in self.selected_symptoms for s in ["Headache", "Dizziness"]):
            recommendations.append("• Rest in a quiet, dark room")
            recommendations.append("• Apply a cold compress to your forehead")
            recommendations.append("• Avoid screens and bright lights")

        if any(s in self.selected_symptoms for s in ["Rash", "Itching"]):
            recommendations.append("• Keep the affected area clean and dry")
            recommendations.append("• Avoid scratching to prevent infection")
            recommendations.append("• Use hypoallergenic moisturizer")

        if any(s in self.selected_symptoms for s in ["Joint Pain", "Muscle Pain"]):
            recommendations.append("• Apply ice for 15-20 minutes, then heat")
            recommendations.append("• Gentle stretching and movement")
            recommendations.append("• Maintain proper posture")

        recommendations.extend([
            "",
            "⚠️ When to seek medical attention:",
            "• If symptoms persist beyond 2 weeks",
            "• If symptoms worsen suddenly",
            "• If you develop new severe symptoms",
            "• Contact your doctor for persistent concerns"
        ])

        text = "\n".join(recommendations)
        self.recommendations_label.configure(text=text)
