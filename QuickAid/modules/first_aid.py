"""
First Aid Guide Module
Complete first aid information for various emergencies
"""

import customtkinter as ctk
import json
from gui.themes import ThemeManager, create_card


class FirstAidPage(ctk.CTkFrame):
    """First Aid Guide page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_content_area()

    def create_sidebar(self):
        """Create condition list sidebar"""
        sidebar = ctk.CTkScrollableFrame(self, width=280)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title = ctk.CTkLabel(
            sidebar,
            text="First Aid Guide",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(pady=20)

        # Search entry
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Search conditions...",
            textvariable=self.search_var,
            height=40,
            corner_radius=10
        )
        search_entry.pack(fill="x", padx=10, pady=10)
        search_entry.bind("<KeyRelease>", self.on_search)

        # Categories
        categories = [
            ("Critical Emergencies", ["Heart Attack", "Stroke", "Choking", "Drowning", "Electric Shock", "Severe Bleeding"]),
            ("Trauma & Injuries", ["Burns", "Cuts and Wounds", "Fractures", "Sprains", "Head Injury"]),
            ("Animal & Insect", ["Snake Bite", "Dog Bite", "Insect Bite/Sting"]),
            ("Medical Emergencies", ["Allergic Reaction", "Asthma Attack", "Seizures", "Diabetic Emergency"]),
            ("Environmental", ["Heat Stroke", "Hypothermia", "Frostbite", "Sunburn"]),
            ("Poisoning", ["Food Poisoning", "Chemical Poisoning", "Drug Overdose"]),
            ("Common Conditions", ["Fever", "Nose Bleeding", "Eye Injury", "Fainting"]),
        ]

        for category_name, conditions in categories:
            # Category header
            cat_label = ctk.CTkLabel(
                sidebar,
                text=category_name,
                font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
                text_color=self.colors["accent"]
            )
            cat_label.pack(anchor="w", padx=10, pady=(15, 5))

            # Condition buttons
            for condition in conditions:
                btn = ctk.CTkButton(
                    sidebar,
                    text=condition,
                    font=ctk.CTkFont(size=11, family="Segoe UI"),
                    fg_color="transparent",
                    text_color=self.colors["text_primary"],
                    hover_color=self.colors["bg_tertiary"],
                    anchor="w",
                    height=30,
                    corner_radius=5,
                    command=lambda c=condition: self.show_condition(c)
                )
                btn.pack(fill="x", padx=10, pady=1)

    def create_content_area(self):
        """Create main content area"""
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["card_bg"],
            corner_radius=15
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Placeholder
        self.placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Select a condition from the list\nfor detailed first aid information",
            font=ctk.CTkFont(size=18, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        self.placeholder.pack(pady=100)

    def on_search(self, event):
        """Handle search"""
        # Placeholder for search functionality
        pass

    def show_condition(self, condition_name):
        """Show condition details"""
        # Clear placeholder
        self.placeholder.pack_forget()

        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Get data from database
        condition_data = self.db.fetchone(
            "SELECT * FROM first_aid_guides WHERE condition_name = ?",
            (condition_name,)
        )

        if condition_data:
            self.display_condition_data(condition_data)
        else:
            # Show default content for conditions not in database
            self.display_default_condition(condition_name)

    def display_condition_data(self, data):
        """Display condition data"""
        # Scrollable content
        content = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Title with severity badge
        title_frame = ctk.CTkFrame(content, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(
            title_frame,
            text=data["condition_name"],
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left")

        # Severity badge
        severity = data["severity"] or "Medium"
        severity_colors = {
            "Critical": "#dc2626",
            "High": "#f59e0b",
            "Medium": "#3b82f6",
            "Low": "#10b981"
        }
        badge_color = severity_colors.get(severity, "#3b82f6")

        severity_badge = ctk.CTkLabel(
            title_frame,
            text=f"  {severity}  ",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color="#ffffff",
            fg_color=badge_color,
            corner_radius=5
        )
        severity_badge.pack(side="right")

        # Category
        category = ctk.CTkLabel(
            content,
            text=f"Category: {data['category'] or 'General'}",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        category.pack(anchor="w", pady=(0, 15))

        # Definition
        if data["definition"]:
            self.create_section(content, "What is it?", data["definition"])

        # Symptoms
        if data["symptoms"]:
            self.create_section(content, "Symptoms", self.format_json(data["symptoms"]))

        # Immediate Action
        if data["immediate_action"]:
            self.create_section(content, "Immediate Action", data["immediate_action"], urgent=True)

        # Step by Step
        if data["step_by_step"]:
            self.create_section(content, "Step-by-Step First Aid", self.format_json(data["step_by_step"]))

        # Do's
        if data["dos"]:
            self.create_section(content, "Do's", self.format_json(data["dos"]), success=True)

        # Don'ts
        if data["donts"]:
            self.create_section(content, "Don'ts", self.format_json(data["donts"]), danger=True)

        # Recovery
        if data["recovery"]:
            self.create_section(content, "Recovery Advice", self.format_json(data["recovery"]))

        # Warning Signs
        if data["warning_signs"]:
            self.create_section(content, "Emergency Warning Signs", self.format_json(data["warning_signs"]), danger=True)

        # Doctor Recommendation
        if data["doctor_recommendation"]:
            self.create_section(content, "When to See a Doctor", data["doctor_recommendation"], info=True)

    def create_section(self, parent, title, content, urgent=False, success=False, danger=False, info=False):
        """Create a content section"""
        if urgent:
            title_color = "#dc2626"
            bg_color = "#fef2f2"
        elif success:
            title_color = "#10b981"
            bg_color = "#f0fdf4"
        elif danger:
            title_color = "#dc2626"
            bg_color = "#fef2f2"
        elif info:
            title_color = "#2563eb"
            bg_color = "#f0f9ff"
        else:
            title_color = self.colors["accent"]
            bg_color = "transparent"

        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=10)

        # Section title
        section_title = ctk.CTkLabel(
            section_frame,
            text=title,
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=title_color
        )
        section_title.pack(anchor="w")

        # Section content
        section_content = ctk.CTkLabel(
            section_frame,
            text=content,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=450
        )
        section_content.pack(anchor="w", pady=(5, 0))

    def format_json(self, json_str):
        """Format JSON string to readable text"""
        try:
            items = json.loads(json_str)
            if isinstance(items, list):
                return "\n".join([f"• {item}" for item in items])
            return str(items)
        except:
            return json_str

    def display_default_condition(self, condition_name):
        """Display default content for conditions not in database"""
        content = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            content,
            text=condition_name,
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(anchor="w", pady=(0, 20))

        # Generic first aid advice
        advice = """First Aid Information:

1. Stay Calm - Assess the situation before acting
2. Ensure Safety - Make sure the area is safe for yourself and the victim
3. Call for Help - Contact emergency services if needed (112)
4. Provide Care - Follow appropriate first aid procedures
5. Monitor - Keep checking the person's condition until help arrives

Remember:
• Do not move an injured person unless in immediate danger
• Do not give food or water to an unconscious person
• Control any bleeding with direct pressure
• Keep the person warm and comfortable
• Document what happened for emergency responders"""

        advice_label = ctk.CTkLabel(
            content,
            text=advice,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=450
        )
        advice_label.pack(anchor="w")
