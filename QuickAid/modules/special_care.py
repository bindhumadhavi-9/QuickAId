"""
Special Care Module
Special care guides for Children, Women, Senior Citizens, Pregnant Women with emergency guidance
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class SpecialCarePage(ctk.CTkFrame):
    """Special Care page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.categories = {
            "Children": {
                "icon": "👶",
                "color": self.theme.get_colors()["info"],
                "guides": [
                    {
                        "title": "Fever in Children",
                        "symptoms": "Temperature above 38°C, weakness, loss of appetite",
                        "care": "Give paracetamol or ibuprofen as per age-appropriate dosage. Ensure adequate fluids. Use tepid sponging if needed. Consult doctor if fever persists.",
                        "emergency": "Seek immediate help if: seizures, stiff neck, difficulty breathing, unconsciousness"
                    },
                    {
                        "title": "Diarrhea in Children",
                        "symptoms": "Loose stools, dehydration, weakness, poor feeding",
                        "care": "Give ORS solution frequently. Maintain breastfeeding if applicable. Provide bland foods like rice, banana. Ensure hand hygiene.",
                        "emergency": "Seek help if: severe dehydration, blood in stool, lethargy, persistent diarrhea beyond 5 days"
                    },
                    {
                        "title": "Choking Prevention",
                        "symptoms": "Difficulty breathing, coughing, inability to speak",
                        "care": "Prevent by avoiding small objects. For choking: use back blows and chest thrusts for infants, Heimlich maneuver for older children.",
                        "emergency": "Call 112 immediately if choking cannot be relieved within seconds"
                    },
                ]
            },
            "Women": {
                "icon": "👩",
                "color": "#8b5cf6",
                "guides": [
                    {
                        "title": "Menstrual Cramps",
                        "symptoms": "Lower abdominal pain, back pain, pelvic discomfort",
                        "care": "Apply heat pad to abdomen. Take ibuprofen or paracetamol. Exercise gently. Maintain hydration. Avoid caffeine.",
                        "emergency": "Seek help if: severe pain preventing daily activities, fever with cramps, unusually heavy bleeding"
                    },
                    {
                        "title": "Breast Pain",
                        "symptoms": "Tenderness, swelling, discomfort",
                        "care": "Wear supportive bra. Apply ice packs. Take pain relievers. Reduce caffeine intake.",
                        "emergency": "Consult doctor if: localized lump, discharge from nipple, persistent one-sided pain"
                    },
                    {
                        "title": "Urinary Tract Infection",
                        "symptoms": "Burning during urination, frequent urination, pelvic pain",
                        "care": "Drink plenty of water. Consume cranberry juice. Avoid irritants. Take antibiotics as prescribed.",
                        "emergency": "Seek help if: fever, blood in urine, severe pain, back pain"
                    },
                ]
            },
            "Pregnant Women": {
                "icon": "🤰",
                "color": self.theme.get_colors()["success"],
                "guides": [
                    {
                        "title": "Nausea and Vomiting",
                        "symptoms": "Morning sickness, weakness, food aversions",
                        "care": "Eat small, frequent meals. Ginger tea or candy may help. Avoid strong smells. Rest adequately.",
                        "emergency": "Seek help if: unable to keep any food down, signs of dehydration, persistent vomiting"
                    },
                    {
                        "title": "Back Pain",
                        "symptoms": "Lower back discomfort, pain worsening with activity",
                        "care": "Use pregnancy pillow. Practice prenatal yoga. Wear flat shoes. Apply warm compress. Maintain good posture.",
                        "emergency": "Consult doctor if: severe pain, pain with contractions, pain accompanied by other symptoms"
                    },
                    {
                        "title": "Edema (Swelling)",
                        "symptoms": "Swelling in feet, ankles, hands",
                        "care": "Elevate legs when resting. Stay hydrated. Wear compression socks. Limit salt. Do gentle exercises.",
                        "emergency": "Seek help if: sudden severe swelling, swelling with headache or vision changes, swelling in face"
                    },
                    {
                        "title": "Emergency Signs",
                        "symptoms": "Vaginal bleeding, severe pain, fluid leakage",
                        "care": "Call emergency services immediately. Do not delay.",
                        "emergency": "Signs requiring immediate help: bleeding, severe abdominal pain, fluid leakage, dizziness, chest pain"
                    },
                ]
            },
            "Senior Citizens": {
                "icon": "👴",
                "color": self.theme.get_colors()["warning"],
                "guides": [
                    {
                        "title": "Fall Prevention",
                        "symptoms": "Balance issues, weakness, dizziness",
                        "care": "Install handrails. Use non-slip flooring. Keep environment well-lit. Use assistive devices. Exercise for strength.",
                        "emergency": "Seek help if: fall occurs, head injury, pain preventing movement, loss of consciousness"
                    },
                    {
                        "title": "Medication Management",
                        "symptoms": "Managing multiple medications, side effects",
                        "care": "Keep medication list updated. Use pill organizer. Take at same time daily. Review with doctor regularly.",
                        "emergency": "Call doctor if: suspected overdose, serious side effects, accidental mixing of medications"
                    },
                    {
                        "title": "Arthritis Management",
                        "symptoms": "Joint pain, stiffness, reduced mobility",
                        "care": "Apply heat therapy. Do gentle exercises. Take prescribed pain medication. Maintain healthy weight.",
                        "emergency": "Seek help if: sudden severe pain, joint swelling with fever, inability to move joint"
                    },
                    {
                        "title": "Memory and Cognitive Issues",
                        "symptoms": "Forgetfulness, confusion, disorientation",
                        "care": "Keep routine schedule. Use reminder systems. Stay mentally active. Sleep adequately. Consult doctor.",
                        "emergency": "Seek immediate help if: sudden confusion, severe memory loss, difficulty recognizing family"
                    },
                ]
            }
        }

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_category_buttons()
        self.create_content_area()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Special Care Guides",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Specialized health guides for different life stages",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_category_buttons(self):
        """Create category selection buttons"""
        button_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        button_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.selected_category = ctk.StringVar(value="Children")

        for idx, (category, data) in enumerate(self.categories.items()):
            btn = ctk.CTkButton(
                button_frame,
                text=f"{data['icon']} {category}",
                command=lambda c=category: self.show_category(c),
                fg_color=data["color"],
                hover_color=self.colors["bg_tertiary"],
                text_color=self.colors["text_primary"],
                font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
                height=45,
                corner_radius=10
            )
            btn.grid(row=0, column=idx, padx=10, pady=15, sticky="ew")

    def create_content_area(self):
        """Create content area"""
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.show_category("Children")

    def show_category(self, category_name):
        """Show guides for selected category"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        category_data = self.categories[category_name]

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=f"{category_data['icon']} {category_name} Care Guides",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=category_data["color"]
        )
        title.pack(anchor="w", pady=(0, 20))

        # Display guides
        for guide in category_data["guides"]:
            self.create_guide_card(guide, category_data["color"])

    def create_guide_card(self, guide, color):
        """Create a care guide card"""
        card = create_card(self.content_frame)
        card.pack(fill="x", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Title
        title = ctk.CTkLabel(
            frame,
            text=guide["title"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=color
        )
        title.pack(anchor="w", pady=(0, 12))

        # Symptoms section
        symptoms_title = ctk.CTkLabel(
            frame,
            text="Symptoms:",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        symptoms_title.pack(anchor="w", pady=(0, 5))

        symptoms_label = ctk.CTkLabel(
            frame,
            text=guide["symptoms"],
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=500
        )
        symptoms_label.pack(anchor="w", pady=(0, 12))

        # Care section
        care_title = ctk.CTkLabel(
            frame,
            text="Care Guidelines:",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        care_title.pack(anchor="w", pady=(0, 5))

        care_label = ctk.CTkLabel(
            frame,
            text=guide["care"],
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=500
        )
        care_label.pack(anchor="w", pady=(0, 12))

        # Emergency section
        emergency_title = ctk.CTkLabel(
            frame,
            text="⚠️ When to Seek Emergency Help:",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            text_color=self.colors["danger"]
        )
        emergency_title.pack(anchor="w", pady=(0, 5))

        emergency_label = ctk.CTkLabel(
            frame,
            text=guide["emergency"],
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["danger"],
            justify="left",
            wraplength=500
        )
        emergency_label.pack(anchor="w")

        # Emergency call button
        def call_emergency():
            # Placeholder for calling emergency services
            pass

        call_btn = ctk.CTkButton(
            frame,
            text="📞 Call Emergency (112)",
            command=call_emergency,
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            text_color="#ffffff",
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            height=32,
            corner_radius=6
        )
        call_btn.pack(anchor="w", pady=(15, 0))
