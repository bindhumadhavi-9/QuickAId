"""
Sidebar Navigation for Quick Aid Application
Professional sidebar with all navigation items
"""

import customtkinter as ctk
from gui.themes import ThemeManager


class Sidebar(ctk.CTkFrame):
    """Sidebar navigation panel"""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent)
        self.navigate = navigate_callback
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.active_button = None
        self.nav_buttons = {}

        self.configure(
            width=250,
            corner_radius=0,
            fg_color=self.colors["bg_secondary"]
        )

        self.grid_rowconfigure(20, weight=1)

        self.create_logo()
        self.create_navigation_items()
        self.create_theme_toggle()
        self.create_footer()

    def create_logo(self):
        """Create application logo header"""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.grid(row=0, column=0, pady=20, padx=15, sticky="ew")

        # Logo icon (using text as placeholder)
        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="+",
            font=ctk.CTkFont(size=32, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        logo_icon.pack(side="left")

        # Logo text
        logo_text = ctk.CTkLabel(
            logo_frame,
            text="QuickAid",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        logo_text.pack(side="left", padx=10)

        # Separator
        separator = ctk.CTkFrame(self, height=2, fg_color=self.colors["border"])
        separator.grid(row=1, column=0, sticky="ew", padx=15, pady=10)

    def create_navigation_items(self):
        """Create navigation buttons"""
        nav_items = [
            ("Dashboard", "dashboard", 2),
            ("Interactive Body", "body_system", 3),
            ("First Aid Guide", "first_aid", 4),
            ("Symptom Checker", "symptom_checker", 5),
            ("Medicine Library", "medicine", 6),
            ("First Aid Kit", "first_aid_kit", 7),
            ("Emergency Contacts", "contacts", 8),
            ("SOS Emergency", "emergency", 9),
            ("Learning Center", "learning", 10),
            ("Health Tools", "health_tools", 11),
            ("Medical Dictionary", "dictionary", 12),
            ("Special Care", "special_care", 13),
        ]

        for text, page, row in nav_items:
            btn = self.create_nav_button(text, page)
            btn.grid(row=row, column=0, padx=10, pady=3, sticky="ew")
            self.nav_buttons[page] = btn

        # Set dashboard as active
        self.set_active("dashboard")

    def create_nav_button(self, text, page):
        """Create a navigation button"""
        btn = ctk.CTkButton(
            self,
            text=text,
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            fg_color="transparent",
            text_color=self.colors["text_primary"],
            hover_color=self.colors["bg_tertiary"],
            anchor="w",
            height=40,
            corner_radius=10,
            command=lambda: self.on_nav_click(page)
        )
        return btn

    def on_nav_click(self, page):
        """Handle navigation click"""
        self.set_active(page)
        self.navigate(page)

    def set_active(self, page):
        """Set active navigation button"""
        # Reset previous active button
        if self.active_button:
            self.nav_buttons[self.active_button].configure(
                fg_color="transparent",
                text_color=self.colors["text_primary"]
            )

        # Set new active button
        self.active_button = page
        if page in self.nav_buttons:
            self.nav_buttons[page].configure(
                fg_color=self.colors["accent"],
                text_color="#ffffff"
            )

    def create_theme_toggle(self):
        """Create theme toggle section"""
        separator = ctk.CTkFrame(self, height=2, fg_color=self.colors["border"])
        separator.grid(row=14, column=0, sticky="ew", padx=15, pady=15)

        # Settings button
        settings_btn = ctk.CTkButton(
            self,
            text="Settings",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            fg_color="transparent",
            text_color=self.colors["text_primary"],
            hover_color=self.colors["bg_tertiary"],
            anchor="w",
            height=40,
            corner_radius=10,
            command=lambda: self.on_nav_click("settings")
        )
        settings_btn.grid(row=15, column=0, padx=10, pady=3, sticky="ew")
        self.nav_buttons["settings"] = settings_btn

    def update_theme_indicator(self, current_theme):
        """Update theme indicator text"""
        pass  # Theme handling is done externally

    def create_footer(self):
        """Create sidebar footer"""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=20, column=0, sticky="sew", pady=15, padx=15)

        version = ctk.CTkLabel(
            footer_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        version.pack()

        credits = ctk.CTkLabel(
            footer_frame,
            text="B.Tech Community Service Project",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        credits.pack(pady=5)
