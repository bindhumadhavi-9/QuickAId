"""
Quick Aid - Smart First Aid & Emergency Care System
Main Entry Point

A complete offline healthcare and first-aid application
Author: B.Tech Community Service Project
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sys
import os
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from gui.dashboard import Dashboard
from gui.sidebar import Sidebar
from gui.themes import ThemeManager, apply_theme
from database.database import DatabaseManager

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class QuickAidApp(ctk.CTk):
    """Main Application Class"""

    def __init__(self):
        super().__init__()

        # Initialize database
        self.db = DatabaseManager()
        self.db.initialize_database()

        # Theme manager
        self.theme_manager = ThemeManager()
        self.current_theme = "dark"

        # Window configuration
        self.title("Quick Aid - Smart First Aid & Emergency Care System")
        self.geometry("1400x900")
        self.minsize(1200, 700)

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.sidebar = Sidebar(self, self.navigate_to)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main content area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Current page
        self.current_page = None

        # Show dashboard by default
        self.navigate_to("dashboard")

        # Protocol for closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def navigate_to(self, page_name):
        """Navigate to different pages"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Import and show the requested page
        if page_name == "dashboard":
            from gui.dashboard import DashboardPage
            self.current_page = DashboardPage(self.content_frame, self.db)
        elif page_name == "body_system":
            from modules.body_system import BodySystemPage
            self.current_page = BodySystemPage(self.content_frame, self.db)
        elif page_name == "first_aid":
            from modules.first_aid import FirstAidPage
            self.current_page = FirstAidPage(self.content_frame, self.db)
        elif page_name == "symptom_checker":
            from modules.symptom_checker import SymptomCheckerPage
            self.current_page = SymptomCheckerPage(self.content_frame, self.db)
        elif page_name == "medicine":
            from modules.medicine_library import MedicineLibraryPage
            self.current_page = MedicineLibraryPage(self.content_frame, self.db)
        elif page_name == "first_aid_kit":
            from modules.first_aid_kit import FirstAidKitPage
            self.current_page = FirstAidKitPage(self.content_frame, self.db)
        elif page_name == "contacts":
            from modules.contacts import ContactsPage
            self.current_page = ContactsPage(self.content_frame, self.db)
        elif page_name == "emergency":
            from modules.emergency import EmergencyPage
            self.current_page = EmergencyPage(self.content_frame, self.db)
        elif page_name == "learning":
            from modules.learning_center import LearningCenterPage
            self.current_page = LearningCenterPage(self.content_frame, self.db)
        elif page_name == "health_tools":
            from modules.health_tools import HealthToolsPage
            self.current_page = HealthToolsPage(self.content_frame, self.db)
        elif page_name == "dictionary":
            from modules.dictionary import DictionaryPage
            self.current_page = DictionaryPage(self.content_frame, self.db)
        elif page_name == "special_care":
            from modules.special_care import SpecialCarePage
            self.current_page = SpecialCarePage(self.content_frame, self.db)
        elif page_name == "settings":
            from gui.settings import SettingsPage
            self.current_page = SettingsPage(self.content_frame, self.db, self.theme_manager, self.toggle_theme)
        else:
            from gui.dashboard import DashboardPage
            self.current_page = DashboardPage(self.content_frame, self.db)

        if self.current_page:
            self.current_page.grid(row=0, column=0, sticky="nsew")

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"

        # Update sidebar theme indicator
        self.sidebar.update_theme_indicator(self.current_theme)

    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Quick Aid?"):
            self.db.close()
            self.destroy()


def main():
    """Main entry point"""
    app = QuickAidApp()

    # Set icon if available
    icon_path = BASE_DIR / "assets" / "icons" / "icon.ico"
    if icon_path.exists():
        app.iconbitmap(str(icon_path))

    app.mainloop()


if __name__ == "__main__":
    main()
