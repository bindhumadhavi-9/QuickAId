"""
Emergency Contacts Module
Add/edit/delete contacts, categories (Family/Doctors/Hospitals/Emergency), call buttons
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class ContactsPage(ctk.CTkFrame):
    """Emergency Contacts page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.contacts = []
        self.selected_contact = None
        self.selected_category = "All"

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_controls()
        self.create_main_content()
        self.load_contacts()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Emergency Contacts",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Manage your emergency contacts and important numbers",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_controls(self):
        """Create control buttons"""
        control_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        control_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        add_btn = ctk.CTkButton(
            control_frame,
            text="+ Add Contact",
            command=self.open_add_contact_dialog,
            fg_color=self.colors["success"],
            hover_color="#059669",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        add_btn.pack(side="left", padx=(20, 10), pady=15)

        edit_btn = ctk.CTkButton(
            control_frame,
            text="✎ Edit",
            command=self.edit_selected_contact,
            fg_color=self.colors["info"],
            hover_color="#0284c7",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        edit_btn.pack(side="left", padx=10, pady=15)

        delete_btn = ctk.CTkButton(
            control_frame,
            text="🗑 Delete",
            command=self.delete_selected_contact,
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        delete_btn.pack(side="left", padx=10, pady=15)

    def create_main_content(self):
        """Create main content area"""
        container = ctk.CTkFrame(self, fg_color=self.colors["bg_primary"])
        container.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_columnconfigure((0, 1), weight=1)
        container.grid_rowconfigure(1, weight=1)

        # Category filter
        filter_frame = ctk.CTkFrame(container, fg_color="transparent")
        filter_frame.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        filter_label = ctk.CTkLabel(
            filter_frame,
            text="Filter by Category:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        filter_label.pack(side="left", padx=(0, 10))

        categories = ["All", "Family", "Doctors", "Hospitals", "Emergency"]
        for cat in categories:
            btn = ctk.CTkButton(
                filter_frame,
                text=cat,
                command=lambda c=cat: self.filter_by_category(c),
                fg_color=self.colors["bg_tertiary"],
                hover_color=self.colors["bg_secondary"],
                font=ctk.CTkFont(size=11, family="Segoe UI"),
                height=30,
                width=80,
                corner_radius=6
            )
            btn.pack(side="left", padx=5)

        # Contacts list
        list_title = ctk.CTkLabel(
            container,
            text="Contacts",
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        list_title.grid(row=1, column=0, sticky="nw", pady=(10, 0))

        self.contacts_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent"
        )
        self.contacts_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=10)

        self.placeholder = ctk.CTkLabel(
            self.contacts_frame,
            text="No contacts added yet.\nClick 'Add Contact' to get started.",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="center"
        )
        self.placeholder.pack(pady=40)

        # Contact details
        details_title = ctk.CTkLabel(
            container,
            text="Contact Details",
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        details_title.grid(row=1, column=1, sticky="nw", pady=(10, 0))

        self.details_frame = create_card(container)
        self.details_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=10)
        self.details_frame.grid_rowconfigure(0, weight=1)

        self.details_content = ctk.CTkScrollableFrame(
            self.details_frame,
            fg_color="transparent"
        )
        self.details_content.pack(fill="both", expand=True, padx=20, pady=20)

        details_placeholder = ctk.CTkLabel(
            self.details_content,
            text="Select a contact to view details",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        details_placeholder.pack(pady=20)

    def load_contacts(self):
        """Load contacts from database or sample data"""
        self.contacts = [
            {"id": 1, "name": "Mom", "category": "Family", "phone": "+91-9876543210", "email": "mom@email.com"},
            {"id": 2, "name": "Dad", "category": "Family", "phone": "+91-9876543211", "email": "dad@email.com"},
            {"id": 3, "name": "Dr. Singh", "category": "Doctors", "phone": "+91-9876543212", "email": "dr.singh@clinic.com"},
            {"id": 4, "name": "City Hospital", "category": "Hospitals", "phone": "+91-9876543213", "email": "info@cityhospital.com"},
            {"id": 5, "name": "Emergency Services", "category": "Emergency", "phone": "112", "email": ""},
        ]
        self.display_contacts()

    def filter_by_category(self, category):
        """Filter contacts by category"""
        self.selected_category = category
        self.display_contacts()

    def display_contacts(self):
        """Display filtered contacts"""
        # Clear placeholder
        self.placeholder.pack_forget()

        # Clear existing
        for widget in self.contacts_frame.winfo_children():
            widget.destroy()

        filtered = [c for c in self.contacts if self.selected_category == "All" or c["category"] == self.selected_category]

        if not filtered:
            self.placeholder.pack(pady=40)
            return

        for contact in filtered:
            self.create_contact_card(contact)

    def create_contact_card(self, contact):
        """Create a contact card"""
        card = create_card(self.contacts_frame)
        card.pack(fill="x", pady=10)

        def on_select():
            self.selected_contact = contact
            self.show_contact_details(contact)

        card.bind("<Button-1>", lambda e: on_select())

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        name = ctk.CTkLabel(
            header,
            text=contact["name"],
            font=ctk.CTkFont(size=13, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name.pack(side="left", anchor="w")

        # Category badge
        category_colors = {
            "Family": self.colors["info"],
            "Doctors": "#8b5cf6",
            "Hospitals": self.colors["danger"],
            "Emergency": "#ef4444"
        }
        badge_color = category_colors.get(contact["category"], self.colors["info"])

        badge = ctk.CTkLabel(
            header,
            text=f"  {contact['category']}  ",
            font=ctk.CTkFont(size=9, family="Segoe UI", weight="bold"),
            text_color="#ffffff",
            fg_color=badge_color,
            corner_radius=4,
            padx=8,
            pady=2
        )
        badge.pack(side="right")

        # Phone
        phone = ctk.CTkLabel(
            frame,
            text=f"📞 {contact['phone']}",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        phone.pack(anchor="w", pady=(0, 5))

        # Email
        if contact["email"]:
            email = ctk.CTkLabel(
                frame,
                text=f"📧 {contact['email']}",
                font=ctk.CTkFont(size=11, family="Segoe UI"),
                text_color=self.colors["text_secondary"]
            )
            email.pack(anchor="w")

    def show_contact_details(self, contact):
        """Show contact details"""
        # Clear details
        for widget in self.details_content.winfo_children():
            widget.destroy()

        # Name
        name_label = ctk.CTkLabel(
            self.details_content,
            text=contact["name"],
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        name_label.pack(anchor="w", pady=(0, 15))

        # Category
        cat_label = ctk.CTkLabel(
            self.details_content,
            text=f"Category: {contact['category']}",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        cat_label.pack(anchor="w", pady=(0, 15))

        # Phone with call button
        phone_frame = ctk.CTkFrame(self.details_content, fg_color="transparent")
        phone_frame.pack(fill="x", pady=10)

        phone_label = ctk.CTkLabel(
            phone_frame,
            text="Phone:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        phone_label.pack(side="left", padx=(0, 10))

        phone_value = ctk.CTkLabel(
            phone_frame,
            text=contact["phone"],
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["accent"]
        )
        phone_value.pack(side="left", expand=True, anchor="w")

        call_btn = ctk.CTkButton(
            phone_frame,
            text="📞 Call",
            command=lambda: self.call_contact(contact),
            fg_color=self.colors["success"],
            hover_color="#059669",
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            height=30,
            width=70,
            corner_radius=6
        )
        call_btn.pack(side="right")

        # Email
        if contact["email"]:
            email_frame = ctk.CTkFrame(self.details_content, fg_color="transparent")
            email_frame.pack(fill="x", pady=10)

            email_label = ctk.CTkLabel(
                email_frame,
                text="Email:",
                font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
                text_color=self.colors["text_primary"]
            )
            email_label.pack(side="left", padx=(0, 10))

            email_value = ctk.CTkLabel(
                email_frame,
                text=contact["email"],
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                text_color=self.colors["accent"]
            )
            email_value.pack(side="left", expand=True, anchor="w")

    def open_add_contact_dialog(self):
        """Open dialog to add new contact"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Emergency Contact")
        dialog.geometry("400x350")
        dialog.configure(fg_color=self.colors["bg_primary"])

        # Name
        name_label = ctk.CTkLabel(
            dialog,
            text="Contact Name:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name_label.pack(anchor="w", padx=20, pady=(20, 5))

        name_entry = ctk.CTkEntry(dialog, placeholder_text="e.g., Mom, Dr. Singh")
        name_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Category
        category_label = ctk.CTkLabel(
            dialog,
            text="Category:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        category_label.pack(anchor="w", padx=20, pady=(0, 5))

        category_var = ctk.StringVar(value="Family")
        category_combo = ctk.CTkComboBox(
            dialog,
            values=["Family", "Doctors", "Hospitals", "Emergency"],
            variable=category_var,
            state="readonly"
        )
        category_combo.pack(fill="x", padx=20, pady=(0, 15))

        # Phone
        phone_label = ctk.CTkLabel(
            dialog,
            text="Phone Number:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        phone_label.pack(anchor="w", padx=20, pady=(0, 5))

        phone_entry = ctk.CTkEntry(dialog, placeholder_text="+91-0000000000")
        phone_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Email
        email_label = ctk.CTkLabel(
            dialog,
            text="Email (Optional):",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        email_label.pack(anchor="w", padx=20, pady=(0, 5))

        email_entry = ctk.CTkEntry(dialog, placeholder_text="email@example.com")
        email_entry.pack(fill="x", padx=20, pady=(0, 20))

        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        def save_contact():
            name = name_entry.get()
            category = category_var.get()
            phone = phone_entry.get()
            email = email_entry.get()

            if name and phone:
                new_contact = {
                    "id": max([c.get("id", 0) for c in self.contacts], default=0) + 1,
                    "name": name,
                    "category": category,
                    "phone": phone,
                    "email": email
                }
                self.contacts.append(new_contact)
                self.display_contacts()
                dialog.destroy()

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=save_contact,
            fg_color=self.colors["success"],
            hover_color="#059669"
        )
        save_btn.pack(side="left", padx=10, fill="x", expand=True)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color=self.colors["bg_tertiary"]
        )
        cancel_btn.pack(side="left", padx=10, fill="x", expand=True)

    def edit_selected_contact(self):
        """Edit selected contact"""
        if not self.selected_contact:
            return
        self.open_add_contact_dialog()

    def delete_selected_contact(self):
        """Delete selected contact"""
        if self.selected_contact and self.selected_contact in self.contacts:
            self.contacts.remove(self.selected_contact)
            self.selected_contact = None
            self.display_contacts()

    def call_contact(self, contact):
        """Call contact"""
        # Placeholder for calling functionality
        pass
