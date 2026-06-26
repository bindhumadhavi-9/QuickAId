"""
Settings Page for Quick Aid Application
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class SettingsPage(ctk.CTkScrollableFrame):
    """Settings configuration page"""

    def __init__(self, parent, db, theme_manager, toggle_theme_callback):
        super().__init__(parent)
        self.db = db
        self.theme_manager = theme_manager
        self.toggle_theme = toggle_theme_callback
        self.colors = self.theme_manager.get_colors()

        self.grid_columnconfigure(0, weight=1)
        self.create_settings()

    def create_settings(self):
        """Create settings sections"""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        header.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Appearance Section
        appearance_card = create_card(self)
        appearance_card.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        appearance_title = ctk.CTkLabel(
            appearance_card,
            text="Appearance",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        appearance_title.pack(anchor="w", padx=15, pady=(15, 10))

        # Theme toggle
        theme_frame = ctk.CTkFrame(appearance_card, fg_color="transparent")
        theme_frame.pack(fill="x", padx=15, pady=10)

        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Theme Mode:",
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_primary"]
        )
        theme_label.pack(side="left")

        self.theme_btn = ctk.CTkButton(
            theme_frame,
            text="Toggle Dark/Light Mode",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["danger"],
            corner_radius=8,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right")

        # Font size slider
        font_frame = ctk.CTkFrame(appearance_card, fg_color="transparent")
        font_frame.pack(fill="x", padx=15, pady=10)

        font_label = ctk.CTkLabel(
            font_frame,
            text="Font Size:",
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_primary"]
        )
        font_label.pack(side="left")

        self.font_slider = ctk.CTkSlider(
            font_frame,
            from_=10,
            to=20,
            number_of_steps=5,
            width=150
        )
        self.font_slider.set(14)
        self.font_slider.pack(side="right")

        # Database Section
        db_card = create_card(self)
        db_card.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        db_title = ctk.CTkLabel(
            db_card,
            text="Database",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        db_title.pack(anchor="w", padx=15, pady=(15, 10))

        # Clear data button
        clear_frame = ctk.CTkFrame(db_card, fg_color="transparent")
        clear_frame.pack(fill="x", padx=15, pady=10)

        clear_label = ctk.CTkLabel(
            clear_frame,
            text="Reset all data:",
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_primary"]
        )
        clear_label.pack(side="left")

        clear_btn = ctk.CTkButton(
            clear_frame,
            text="Reset Database",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            corner_radius=8,
            command=self.confirm_reset
        )
        clear_btn.pack(side="right")

        # About Section
        about_card = create_card(self)
        about_card.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        about_title = ctk.CTkLabel(
            about_card,
            text="About Quick Aid",
            font=ctk.CTkFont(size=16, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        about_title.pack(anchor="w", padx=15, pady=(15, 10))

        about_text = ctk.CTkLabel(
            about_card,
            text="Quick Aid - Smart First Aid & Emergency Care System\n\n"
                 "A comprehensive offline healthcare application for first aid guidance, "
                 "emergency management, and medical information.\n\n"
                 "Developed as a B.Tech Community Service Project",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=500
        )
        about_text.pack(anchor="w", padx=15, pady=(0, 15))

    def confirm_reset(self):
        """Confirm database reset"""
        import tkinter as tk
        from tkinter import messagebox
        if messagebox.askyesno("Reset Database", "Are you sure you want to reset all data? This cannot be undone."):
            self.db.execute("DELETE FROM emergency_contacts WHERE is_primary = 0")
            self.db.execute("DELETE FROM first_aid_kit_items")
            self.db.execute("DELETE FROM quiz_scores")
            self.db.execute("DELETE FROM health_calculations")
            messagebox.showinfo("Success", "User data has been reset.")
