"""
Medical Dictionary Module
Medical dictionary with search functionality, term definitions, explanations
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class DictionaryPage(ctk.CTkFrame):
    """Medical Dictionary page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.terms = []
        self.filtered_terms = []

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_search_area()
        self.create_main_content()
        self.load_terms()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Medical Dictionary",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Search and learn medical terms and definitions",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_search_area(self):
        """Create search area"""
        search_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        search_label.pack(side="left", padx=(20, 10), pady=15)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search medical terms...",
            textvariable=self.search_var,
            height=40,
            corner_radius=10
        )
        search_entry.pack(side="left", padx=10, pady=15, fill="x", expand=True)
        search_entry.bind("<KeyRelease>", self.on_search)

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
        # Left column - Terms list
        left_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        left_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=20)
        left_frame.grid_columnconfigure(0, weight=1)

        list_title = ctk.CTkLabel(
            left_frame,
            text="Medical Terms",
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        list_title.pack(anchor="w", pady=(0, 15))

        self.terms_list_frame = ctk.CTkScrollableFrame(
            left_frame,
            fg_color="transparent"
        )
        self.terms_list_frame.pack(fill="both", expand=True)

        # Right column - Term details
        right_frame = create_card(self)
        right_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 20), pady=20)
        right_frame.grid_rowconfigure(1, weight=1)

        details_title = ctk.CTkLabel(
            right_frame,
            text="Term Details",
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
            text="Select a term to view its definition and explanation",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        self.placeholder.pack(pady=20)

    def load_terms(self):
        """Load medical terms"""
        self.terms = [
            {
                "term": "Abdomen",
                "definition": "The area of the body below the rib cage and above the pelvis",
                "explanation": "The abdomen contains organs like the stomach, intestines, liver, and pancreas. Pain in this area should be evaluated by a doctor.",
                "related": ["Abdominal pain", "Stomach", "Organs"]
            },
            {
                "term": "Acute",
                "definition": "Sudden onset with severe symptoms; not chronic",
                "explanation": "Acute conditions develop quickly and are usually more severe. Examples include acute appendicitis or acute bronchitis.",
                "related": ["Chronic", "Symptoms", "Disease"]
            },
            {
                "term": "Allergy",
                "definition": "An abnormal immune response to a substance that is harmless to most people",
                "explanation": "Allergies can cause symptoms like sneezing, itching, rash, or anaphylaxis. Common allergens include pollen, dust, food, and pet dander.",
                "related": ["Immune system", "Anaphylaxis", "Antihistamine"]
            },
            {
                "term": "Anaphylaxis",
                "definition": "A severe, potentially life-threatening allergic reaction that occurs rapidly",
                "explanation": "Anaphylaxis requires immediate medical attention and emergency epinephrine injection. Symptoms include difficulty breathing, swelling, and drop in blood pressure.",
                "related": ["Allergy", "Emergency", "EpiPen"]
            },
            {
                "term": "Antibiotic",
                "definition": "A substance that kills or inhibits the growth of bacteria",
                "explanation": "Antibiotics are used to treat bacterial infections. They do not work against viral infections like colds or flu.",
                "related": ["Bacteria", "Infection", "Drug"]
            },
            {
                "term": "Artery",
                "definition": "A blood vessel that carries blood away from the heart",
                "explanation": "Arteries carry oxygenated blood to all parts of the body. They have thick, elastic walls to handle high pressure.",
                "related": ["Vein", "Blood vessel", "Circulation"]
            },
            {
                "term": "Asthma",
                "definition": "A chronic respiratory disease characterized by airway inflammation and narrowing",
                "explanation": "Asthma causes wheezing, shortness of breath, chest tightness, and coughing, especially at night or during exercise. It's managed with inhalers and medications.",
                "related": ["Breathing", "Chronic", "Inhaler"]
            },
            {
                "term": "Benign",
                "definition": "Not cancerous and usually not dangerous",
                "explanation": "Benign tumors or growths do not spread and are typically not life-threatening, unlike malignant (cancerous) growths.",
                "related": ["Malignant", "Cancer", "Tumor"]
            },
            {
                "term": "Bilateral",
                "definition": "Affecting both sides of the body or an organ",
                "explanation": "For example, bilateral pneumonia affects both lungs. Unilateral means affecting only one side.",
                "related": ["Unilateral", "Symmetry", "Body"]
            },
            {
                "term": "Biopsy",
                "definition": "A procedure where a sample of tissue is taken for examination",
                "explanation": "Biopsies are often used to diagnose cancer or other diseases by examining cells under a microscope.",
                "related": ["Cancer", "Pathology", "Diagnosis"]
            },
            {
                "term": "Blood Pressure",
                "definition": "The force exerted by blood against the walls of blood vessels",
                "explanation": "Measured in mmHg with two numbers: systolic (top) and diastolic (bottom). Normal is less than 120/80. High blood pressure increases heart disease and stroke risk.",
                "related": ["Hypertension", "Heart", "Circulation"]
            },
            {
                "term": "Chronic",
                "definition": "Long-lasting, typically more than 3 months; not acute",
                "explanation": "Chronic conditions develop slowly and persist over time. Examples include diabetes, asthma, and arthritis.",
                "related": ["Acute", "Disease", "Long-term"]
            },
            {
                "term": "Contusion",
                "definition": "A bruise; an injury where blood vessels are damaged but skin is not broken",
                "explanation": "Contusions cause discoloration, swelling, and pain. Most minor contusions heal on their own with rest and ice.",
                "related": ["Bruise", "Injury", "Swelling"]
            },
            {
                "term": "Diagnosis",
                "definition": "The identification of a disease or condition",
                "explanation": "Diagnosis is made through medical examination, tests, and evaluation of symptoms to determine what is causing the problem.",
                "related": ["Disease", "Symptoms", "Treatment"]
            },
            {
                "term": "Edema",
                "definition": "Abnormal accumulation of fluid in body tissues causing swelling",
                "explanation": "Edema can result from injury, infection, kidney disease, heart problems, or other conditions. It's often seen in legs and ankles.",
                "related": ["Swelling", "Fluid", "Lymphatic"]
            },
            {
                "term": "Epidemic",
                "definition": "A widespread occurrence of a disease in a community at a particular time",
                "explanation": "An epidemic affects many people in an area. A pandemic is a global epidemic.",
                "related": ["Pandemic", "Disease", "Contagious"]
            },
            {
                "term": "Fever",
                "definition": "An abnormally high body temperature, typically above 38°C (100.4°F)",
                "explanation": "Fever is the body's response to infection or inflammation. Most fevers are beneficial as they help fight infection.",
                "related": ["Temperature", "Infection", "Symptom"]
            },
            {
                "term": "Fracture",
                "definition": "A break in a bone",
                "explanation": "Fractures can be simple (bone intact under skin) or compound (bone breaks through skin). Treatment depends on severity and location.",
                "related": ["Bone", "Injury", "Break"]
            },
            {
                "term": "Gastritis",
                "definition": "Inflammation of the stomach lining",
                "explanation": "Gastritis causes stomach pain, nausea, and vomiting. It can be caused by bacteria, stress, or certain medications.",
                "related": ["Stomach", "Inflammation", "Ulcer"]
            },
            {
                "term": "Gene",
                "definition": "A unit of hereditary information that controls inherited traits",
                "explanation": "Genes are made of DNA and determine characteristics like eye color, height, and susceptibility to certain diseases.",
                "related": ["DNA", "Heredity", "Genetics"]
            },
        ]
        self.filtered_terms = self.terms
        self.display_terms_list()

    def on_search(self, event=None):
        """Filter terms based on search"""
        search_term = self.search_var.get().lower()

        self.filtered_terms = [
            term for term in self.terms
            if search_term in term["term"].lower() or
            search_term in term["definition"].lower()
        ]

        self.display_terms_list()
        self.clear_details()

    def clear_search(self):
        """Clear search"""
        self.search_var.set("")
        self.filtered_terms = self.terms
        self.display_terms_list()
        self.clear_details()

    def display_terms_list(self):
        """Display list of terms"""
        # Clear existing
        for widget in self.terms_list_frame.winfo_children():
            widget.destroy()

        if not self.filtered_terms:
            no_results = ctk.CTkLabel(
                self.terms_list_frame,
                text="No terms found",
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                text_color=self.colors["text_secondary"]
            )
            no_results.pack(pady=20)
            return

        # Sort alphabetically
        sorted_terms = sorted(self.filtered_terms, key=lambda x: x["term"])

        for term_data in sorted_terms:
            self.create_term_item(term_data)

    def create_term_item(self, term_data):
        """Create a term list item"""
        item = create_card(self.terms_list_frame)
        item.pack(fill="x", pady=8)

        button = ctk.CTkButton(
            item,
            text="",
            fg_color="transparent",
            hover_color=self.colors["bg_tertiary"],
            corner_radius=10,
            height=50,
            command=lambda t=term_data: self.show_term_details(t)
        )
        button.pack(fill="both", expand=True, padx=15, pady=12)

        # Content inside button
        frame = ctk.CTkFrame(button, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        name = ctk.CTkLabel(
            frame,
            text=term_data["term"],
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name.pack(anchor="w")

        definition = ctk.CTkLabel(
            frame,
            text=term_data["definition"],
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=200
        )
        definition.pack(anchor="w", pady=(3, 0))

    def show_term_details(self, term_data):
        """Show term details"""
        self.placeholder.pack_forget()

        # Clear existing
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Term name
        name_label = ctk.CTkLabel(
            self.details_frame,
            text=term_data["term"],
            font=ctk.CTkFont(size=18, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        name_label.pack(anchor="w", pady=(0, 15))

        # Definition
        def_title = ctk.CTkLabel(
            self.details_frame,
            text="Definition:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        def_title.pack(anchor="w", pady=(0, 5))

        def_label = ctk.CTkLabel(
            self.details_frame,
            text=term_data["definition"],
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=280
        )
        def_label.pack(anchor="w", pady=(0, 15))

        # Explanation
        exp_title = ctk.CTkLabel(
            self.details_frame,
            text="Explanation:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        exp_title.pack(anchor="w", pady=(0, 5))

        exp_label = ctk.CTkLabel(
            self.details_frame,
            text=term_data["explanation"],
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=280
        )
        exp_label.pack(anchor="w", pady=(0, 15))

        # Related terms
        if term_data.get("related"):
            rel_title = ctk.CTkLabel(
                self.details_frame,
                text="Related Terms:",
                font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
                text_color=self.colors["text_primary"]
            )
            rel_title.pack(anchor="w", pady=(0, 8))

            for related in term_data["related"]:
                rel_label = ctk.CTkLabel(
                    self.details_frame,
                    text=f"• {related}",
                    font=ctk.CTkFont(size=10, family="Segoe UI"),
                    text_color=self.colors["accent"]
                )
                rel_label.pack(anchor="w")

    def clear_details(self):
        """Clear details pane"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.placeholder.pack(pady=20)
