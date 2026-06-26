"""
Dashboard Page for Quick Aid Application
Main landing page with overview and quick actions
"""

import customtkinter as ctk
from tkinter import messagebox
import json
from datetime import datetime
from gui.themes import ThemeManager, create_card, create_styled_button


class DashboardPage(ctk.CTkScrollableFrame):
    """Dashboard landing page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.create_header()
        self.create_quick_actions()
        self.create_stats_cards()
        self.create_emergency_contacts_widget()
        self.create_kit_status_widget()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 20), padx=10)
        header.grid_columnconfigure(1, weight=1)

        # Left side - Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")

        title = ctk.CTkLabel(
            title_frame,
            text="Quick Aid",
            font=ctk.CTkFont(size=32, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            title_frame,
            text="  - Smart First Aid & Emergency Care System",
            font=ctk.CTkFont(size=16, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left")

        # Right side - Date and greeting
        date_frame = ctk.CTkFrame(header, fg_color="transparent")
        date_frame.grid(row=0, column=1, sticky="e")

        current_date = datetime.now().strftime("%A, %B %d, %Y")
        date_label = ctk.CTkLabel(
            date_frame,
            text=current_date,
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        date_label.pack(side="right")

    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10, padx=10)
        actions_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        quick_actions = [
            ("SOS Emergency", "red", "emergency"),
            ("Body Map", "blue", "body_system"),
            ("Symptoms", "green", "symptom_checker"),
            ("First Aid", "orange", "first_aid"),
            ("Medicines", "purple", "medicine"),
        ]

        for i, (text, color, page) in enumerate(quick_actions):
            if color == "red":
                button_color = "#dc2626"
                hover = "#b91c1c"
            elif color == "blue":
                button_color = "#2563eb"
                hover = "#1d4ed8"
            elif color == "green":
                button_color = "#059669"
                hover = "#047857"
            elif color == "orange":
                button_color = "#d97706"
                hover = "#b45309"
            else:
                button_color = "#7c3aed"
                hover = "#6d28d9"

            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
                fg_color=button_color,
                hover_color=hover,
                corner_radius=12,
                height=50
            )
            btn.grid(row=0, column=i, padx=5, sticky="ew")

    def create_stats_cards(self):
        """Create statistics cards"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=15, padx=10)
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Get stats from database
        contacts_count = len(self.db.fetchall("SELECT * FROM emergency_contacts"))
        kit_items = self.db.fetchall("SELECT * FROM first_aid_kit_items")
        in_stock = sum(1 for item in kit_items if item["in_stock"] == 1)
        quiz_scores = self.db.fetchall("SELECT * FROM quiz_scores")

        stats = [
            ("Emergency Contacts", str(contacts_count), "#dc2626", "contacts"),
            ("Kit Items In Stock", f"{in_stock}/{len(kit_items)}", "#10b981", "kit"),
            ("Quizzes Completed", str(len(quiz_scores)), "#2563eb", "quiz"),
            ("Articles Read", "12", "#7c3aed", "articles"),
        ]

        for i, (title, value, color, icon_type) in enumerate(stats):
            card = create_card(stats_frame)
            card.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

            # Title
            title_lbl = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                text_color=self.colors["text_secondary"]
            )
            title_lbl.pack(pady=(15, 5), padx=15)

            # Value
            value_lbl = ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
                text_color=color
            )
            value_lbl.pack(pady=(0, 15), padx=15)

    def create_emergency_contacts_widget(self):
        """Create emergency contacts widget"""
        card = create_card(self)
        card.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10, padx=10)

        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))

        title = ctk.CTkLabel(
            header,
            text="Emergency Contacts",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left")

        # Get contacts
        contacts = self.db.fetchall("SELECT * FROM emergency_contacts WHERE is_primary = 1 LIMIT 4")

        for contact in contacts:
            contact_frame = ctk.CTkFrame(card, fg_color="transparent")
            contact_frame.pack(fill="x", padx=15, pady=5)

            name = ctk.CTkLabel(
                contact_frame,
                text=contact["name"],
                font=ctk.CTkFont(size=13, family="Segoe UI"),
                text_color=self.colors["text_primary"]
            )
            name.pack(side="left")

            phone = ctk.CTkLabel(
                contact_frame,
                text=contact["phone"],
                font=ctk.CTkFont(size=13, family="Segoe UI"),
                text_color=self.colors["accent"]
            )
            phone.pack(side="right")

    def create_kit_status_widget(self):
        """Create first aid kit status widget"""
        card = create_card(self)
        card.grid(row=3, column=2, columnspan=2, sticky="nsew", pady=10, padx=10)

        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))

        title = ctk.CTkLabel(
            header,
            text="First Aid Kit Status",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left")

        # Get items
        items = self.db.fetchall("SELECT * FROM first_aid_kit_items LIMIT 5")

        if not items:
            # Show default items
            default_items = ["Bandages", "Antiseptic", "Gloves", "Scissors", "Cotton"]
            for item_name in default_items:
                item_frame = ctk.CTkFrame(card, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=5)

                name = ctk.CTkLabel(
                    item_frame,
                    text=item_name,
                    font=ctk.CTkFont(size=13, family="Segoe UI"),
                    text_color=self.colors["text_primary"]
                )
                name.pack(side="left")

                status = ctk.CTkLabel(
                    item_frame,
                    text="Add to Kit",
                    font=ctk.CTkFont(size=11, family="Segoe UI"),
                    text_color=self.colors["warning"]
                )
                status.pack(side="right")
        else:
            for item in items:
                item_frame = ctk.CTkFrame(card, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=5)

                name = ctk.CTkLabel(
                    item_frame,
                    text=item["name"],
                    font=ctk.CTkFont(size=13, family="Segoe UI"),
                    text_color=self.colors["text_primary"]
                )
                name.pack(side="left")

                status_color = self.colors["success"] if item["in_stock"] == 1 else self.colors["danger"]
                status = ctk.CTkLabel(
                    item_frame,
                    text="In Stock" if item["in_stock"] == 1 else "Missing",
                    font=ctk.CTkFont(size=11, family="Segoe UI"),
                    text_color=status_color
                )
                status.pack(side="right")


class Dashboard:
    """Dashboard component placeholder"""
    pass
