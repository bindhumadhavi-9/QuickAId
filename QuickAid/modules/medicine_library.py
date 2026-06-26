"""
Medicine Library Module
Searchable medicine database with comprehensive medicine information
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class MedicineLibraryPage(ctk.CTkFrame):
    """Medicine Library page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.medicines = []
        self.filtered_medicines = []

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_search_area()
        self.create_main_content()
        self.load_medicines()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Medicine Library",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Search and learn about medicines, dosage, side effects, and warnings",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_search_area(self):
        """Create search and filter area"""
        search_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))

        # Search entry
        search_label = ctk.CTkLabel(
            search_frame,
            text="Search Medicine:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        search_label.pack(side="left", padx=(20, 10), pady=15)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Medicine name, category, or use...",
            textvariable=self.search_var,
            height=40,
            corner_radius=10,
            width=300
        )
        search_entry.pack(side="left", padx=10, pady=15, fill="x", expand=True)
        search_entry.bind("<KeyRelease>", self.on_search)

        # Filter by category
        category_label = ctk.CTkLabel(
            search_frame,
            text="Category:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        category_label.pack(side="left", padx=(20, 10))

        self.category_var = ctk.StringVar(value="All")
        categories = ["All", "Painkillers", "Antibiotics", "Antihistamines", "Antacids", "Vitamins"]
        category_dropdown = ctk.CTkComboBox(
            search_frame,
            values=categories,
            variable=self.category_var,
            state="readonly",
            height=40,
            corner_radius=10,
            width=150,
            command=self.on_search
        )
        category_dropdown.pack(side="left", padx=10, pady=15)

        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_search,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_secondary"],
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            width=80,
            height=40,
            corner_radius=8
        )
        clear_btn.pack(side="right", padx=20, pady=15)

    def create_main_content(self):
        """Create main content area"""
        # Left column - Medicine list
        left_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        left_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=20)
        left_frame.grid_columnconfigure(0, weight=1)

        list_title = ctk.CTkLabel(
            left_frame,
            text="Available Medicines",
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        list_title.pack(anchor="w", pady=(0, 15))

        self.medicines_list_frame = ctk.CTkScrollableFrame(
            left_frame,
            fg_color="transparent"
        )
        self.medicines_list_frame.pack(fill="both", expand=True)

        # Right column - Medicine details
        right_frame = create_card(self)
        right_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 20), pady=20)
        right_frame.grid_rowconfigure(1, weight=1)

        details_title = ctk.CTkLabel(
            right_frame,
            text="Medicine Details",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        details_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.details_frame = ctk.CTkScrollableFrame(
            right_frame,
            fg_color="transparent"
        )
        self.details_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Placeholder
        self.placeholder = ctk.CTkLabel(
            self.details_frame,
            text="Select a medicine to view details",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        self.placeholder.pack(pady=20)

    def load_medicines(self):
        """Load medicines from database or create sample data"""
        self.medicines = [
            {
                "name": "Paracetamol",
                "category": "Painkillers",
                "uses": "Fever, headache, mild to moderate pain",
                "dosage": "500-1000 mg every 4-6 hours, max 4000 mg/day",
                "side_effects": "Rare: liver damage with overdose, allergic reactions",
                "warnings": "Do not exceed maximum daily dose; avoid with alcohol; caution in liver disease",
                "storage": "Room temperature, dry place, away from light"
            },
            {
                "name": "Ibuprofen",
                "category": "Painkillers",
                "uses": "Pain relief, fever, inflammation, arthritis",
                "dosage": "200-400 mg every 4-6 hours, max 1200 mg/day",
                "side_effects": "Stomach upset, heartburn, dizziness, rash",
                "warnings": "Take with food or milk; avoid if allergic to NSAIDs; risk of GI bleeding",
                "storage": "Room temperature, keep in original container"
            },
            {
                "name": "Aspirin",
                "category": "Painkillers",
                "uses": "Pain relief, fever, heart attack prevention, blood thinner",
                "dosage": "300-900 mg every 4-6 hours for pain; 75-325 mg daily for heart health",
                "side_effects": "Stomach irritation, nausea, increased bleeding risk",
                "warnings": "Not for children under 12 for viral illness; increases bleeding risk; caution with anticoagulants",
                "storage": "Cool, dry place away from moisture"
            },
            {
                "name": "Amoxicillin",
                "category": "Antibiotics",
                "uses": "Bacterial infections: ear, throat, urinary tract, skin",
                "dosage": "250-500 mg three times daily for 7-10 days",
                "side_effects": "Nausea, vomiting, rash, diarrhea, allergic reactions",
                "warnings": "Do not use if allergic to penicillin; complete full course; may reduce birth control effectiveness",
                "storage": "Refrigerate if prescribed as liquid; tablets at room temperature"
            },
            {
                "name": "Cetirizine",
                "category": "Antihistamines",
                "uses": "Allergies, hay fever, itching, hives, allergic rhinitis",
                "dosage": "10 mg once daily",
                "side_effects": "Drowsiness, dry mouth, headache, fatigue",
                "warnings": "May cause drowsiness; avoid operating machinery; caution with liver disease",
                "storage": "Room temperature, away from moisture and light"
            },
            {
                "name": "Omeprazole",
                "category": "Antacids",
                "uses": "Acid reflux, GERD, ulcers, heartburn prevention",
                "dosage": "20-40 mg once daily, preferably before breakfast",
                "side_effects": "Headache, nausea, stomach pain, constipation",
                "warnings": "Long-term use may reduce B12 and calcium absorption; can affect other drug absorption",
                "storage": "Room temperature in original container"
            },
            {
                "name": "Vitamin C (Ascorbic Acid)",
                "category": "Vitamins",
                "uses": "Immune system support, wound healing, antioxidant",
                "dosage": "500-2000 mg daily in divided doses",
                "side_effects": "Nausea, diarrhea, kidney stones (in susceptible individuals)",
                "warnings": "Excess intake may cause diarrhea; caution in kidney disease; may interfere with lab tests",
                "storage": "Cool, dry place; avoid direct sunlight"
            },
            {
                "name": "Vitamin D3",
                "category": "Vitamins",
                "uses": "Bone health, calcium absorption, immune function",
                "dosage": "400-2000 IU daily",
                "side_effects": "Rare: nausea, weakness, kidney stones with excessive intake",
                "warnings": "Avoid overdosing; consult doctor if taking thiazide diuretics; may take months to build up levels",
                "storage": "Room temperature, away from light"
            },
        ]
        self.filtered_medicines = self.medicines
        self.display_medicines_list()

    def on_search(self, event=None):
        """Filter medicines based on search and category"""
        search_term = self.search_var.get().lower()
        category_filter = self.category_var.get()

        self.filtered_medicines = [
            med for med in self.medicines
            if (search_term in med["name"].lower() or
                search_term in med["uses"].lower() or
                search_term in med["category"].lower()) and
            (category_filter == "All" or med["category"] == category_filter)
        ]

        self.display_medicines_list()
        self.clear_details()

    def clear_search(self):
        """Clear search and filters"""
        self.search_var.set("")
        self.category_var.set("All")
        self.filtered_medicines = self.medicines
        self.display_medicines_list()
        self.clear_details()

    def display_medicines_list(self):
        """Display list of filtered medicines"""
        # Clear existing
        for widget in self.medicines_list_frame.winfo_children():
            widget.destroy()

        if not self.filtered_medicines:
            no_results = ctk.CTkLabel(
                self.medicines_list_frame,
                text="No medicines found",
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                text_color=self.colors["text_secondary"]
            )
            no_results.pack(pady=20)
            return

        for medicine in self.filtered_medicines:
            self.create_medicine_item(medicine)

    def create_medicine_item(self, medicine):
        """Create a medicine list item"""
        item = create_card(self.medicines_list_frame)
        item.pack(fill="x", pady=8)

        button = ctk.CTkButton(
            item,
            text="",
            fg_color="transparent",
            hover_color=self.colors["bg_tertiary"],
            corner_radius=10,
            height=60,
            command=lambda m=medicine: self.show_medicine_details(m)
        )
        button.pack(fill="both", expand=True, padx=15, pady=12)

        # Content inside button
        frame = ctk.CTkFrame(button, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        name = ctk.CTkLabel(
            frame,
            text=medicine["name"],
            font=ctk.CTkFont(size=13, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name.pack(anchor="w")

        category = ctk.CTkLabel(
            frame,
            text=f"Category: {medicine['category']}",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        category.pack(anchor="w", pady=(3, 0))

    def show_medicine_details(self, medicine):
        """Show medicine details"""
        self.placeholder.pack_forget()

        # Clear existing
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Medicine name
        name_label = ctk.CTkLabel(
            self.details_frame,
            text=medicine["name"],
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        name_label.pack(anchor="w", pady=(0, 15))

        # Category badge
        category_badge = ctk.CTkLabel(
            self.details_frame,
            text=f"  {medicine['category']}  ",
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            text_color="#ffffff",
            fg_color=self.colors["info"],
            corner_radius=5,
            padx=10,
            pady=5
        )
        category_badge.pack(anchor="w", pady=(0, 15))

        # Sections
        self.create_detail_section("Uses", medicine["uses"])
        self.create_detail_section("Dosage", medicine["dosage"])
        self.create_detail_section("Side Effects", medicine["side_effects"])
        self.create_detail_section("Warnings", medicine["warnings"], urgent=True)
        self.create_detail_section("Storage", medicine["storage"])

    def create_detail_section(self, title, content, urgent=False):
        """Create a detail section"""
        section = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        section.pack(fill="x", pady=15)

        title_color = self.colors["danger"] if urgent else self.colors["accent"]

        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=title_color
        )
        title_label.pack(anchor="w", pady=(0, 8))

        content_label = ctk.CTkLabel(
            section,
            text=content,
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=280
        )
        content_label.pack(anchor="w")

    def clear_details(self):
        """Clear details pane"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.placeholder.pack(pady=20)
