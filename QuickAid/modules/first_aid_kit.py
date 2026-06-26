"""
First Aid Kit Manager Module
Item tracking, add/edit/delete items, check in/out stock, completion percentage
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card
from datetime import datetime, timedelta


class FirstAidKitPage(ctk.CTkFrame):
    """First Aid Kit Manager page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.kit_items = []
        self.selected_item = None

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_controls()
        self.create_main_content()
        self.load_kit_items()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=100)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header,
            text="First Aid Kit Manager",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Completion status
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e", padx=20)

        self.completion_label = ctk.CTkLabel(
            status_frame,
            text="Completion: 0%",
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        self.completion_label.pack(side="left", padx=10)

        self.completion_bar = ctk.CTkProgressBar(
            status_frame,
            value=0,
            height=8,
            fg_color=self.colors["bg_tertiary"],
            progress_color=self.colors["success"],
            width=200
        )
        self.completion_bar.pack(side="left", padx=10)

    def create_controls(self):
        """Create control buttons"""
        control_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        control_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        add_btn = ctk.CTkButton(
            control_frame,
            text="+ Add Item",
            command=self.open_add_item_dialog,
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
            command=self.edit_selected_item,
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
            command=self.delete_selected_item,
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        delete_btn.pack(side="left", padx=10, pady=15)

        refresh_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Refresh",
            command=self.load_kit_items,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_secondary"],
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            height=40,
            corner_radius=8
        )
        refresh_btn.pack(side="left", padx=10, pady=15)

    def create_main_content(self):
        """Create main content area"""
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        container.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)

        # Items list
        title = ctk.CTkLabel(
            container,
            text="Kit Items",
            font=ctk.CTkFont(size=18, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 15))

        self.items_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent"
        )
        self.items_frame.pack(fill="both", expand=True)

        # Placeholder
        self.placeholder = ctk.CTkLabel(
            self.items_frame,
            text="No items in kit. Click 'Add Item' to get started.",
            font=ctk.CTkFont(size=13, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        self.placeholder.pack(pady=40)

    def load_kit_items(self):
        """Load kit items from database"""
        # Sample data
        self.kit_items = [
            {
                "id": 1,
                "name": "Adhesive Bandages",
                "category": "Wound Care",
                "quantity": 50,
                "stock": 40,
                "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "status": "Good"
            },
            {
                "id": 2,
                "name": "Gauze Pads",
                "category": "Wound Care",
                "quantity": 20,
                "stock": 18,
                "expiry_date": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
                "status": "Good"
            },
            {
                "id": 3,
                "name": "Antibiotic Ointment",
                "category": "Wound Care",
                "quantity": 5,
                "stock": 4,
                "expiry_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                "status": "Warning"
            },
            {
                "id": 4,
                "name": "Pain Relief Tablets",
                "category": "Medication",
                "quantity": 30,
                "stock": 22,
                "expiry_date": (datetime.now() + timedelta(days=200)).strftime("%Y-%m-%d"),
                "status": "Good"
            },
            {
                "id": 5,
                "name": "Thermometer",
                "category": "Equipment",
                "quantity": 1,
                "stock": 1,
                "expiry_date": (datetime.now() + timedelta(days=730)).strftime("%Y-%m-%d"),
                "status": "Good"
            },
        ]
        self.display_kit_items()

    def display_kit_items(self):
        """Display kit items"""
        # Clear placeholder
        self.placeholder.pack_forget()

        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        if not self.kit_items:
            self.placeholder.pack(pady=40)
            return

        for item in self.kit_items:
            self.create_item_card(item)

        # Update completion percentage
        self.update_completion()

    def create_item_card(self, item):
        """Create an item card"""
        card = create_card(self.items_frame)
        card.pack(fill="x", pady=10)

        # Make card clickable
        def on_card_click(event=None):
            self.selected_item = item
            self.highlight_selected()

        card.bind("<Button-1>", on_card_click)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Item header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        name = ctk.CTkLabel(
            header,
            text=item["name"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name.pack(side="left", anchor="w")

        category = ctk.CTkLabel(
            header,
            text=f"  {item['category']}  ",
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            text_color="#ffffff",
            fg_color=self.colors["info"],
            corner_radius=5,
            padx=10,
            pady=2
        )
        category.pack(side="left", padx=10)

        # Status badge
        status_color = self.colors["success"] if item["status"] == "Good" else self.colors["warning"]
        status_badge = ctk.CTkLabel(
            header,
            text=f"  {item['status']}  ",
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            text_color="#ffffff",
            fg_color=status_color,
            corner_radius=5,
            padx=10,
            pady=2
        )
        status_badge.pack(side="right")

        # Stock info
        info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=8)

        stock_label = ctk.CTkLabel(
            info_frame,
            text=f"Stock: {item['stock']}/{item['quantity']}",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        stock_label.pack(side="left", anchor="w")

        expiry_label = ctk.CTkLabel(
            info_frame,
            text=f"Expiry: {item['expiry_date']}",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        expiry_label.pack(side="right")

        # Progress bar
        progress_value = item['stock'] / item['quantity'] if item['quantity'] > 0 else 0
        progress = ctk.CTkProgressBar(
            frame,
            value=progress_value,
            height=6,
            fg_color=self.colors["bg_tertiary"],
            progress_color=self.colors["success"]
        )
        progress.pack(fill="x", pady=8)

        # Action buttons
        actions_frame = ctk.CTkFrame(frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(8, 0))

        checkout_btn = ctk.CTkButton(
            actions_frame,
            text="➖ Check Out",
            command=lambda: self.checkout_item(item),
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            height=28,
            width=100,
            corner_radius=6
        )
        checkout_btn.pack(side="left", padx=(0, 10))

        checkin_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Check In",
            command=lambda: self.checkin_item(item),
            fg_color=self.colors["success"],
            hover_color="#059669",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            height=28,
            width=100,
            corner_radius=6
        )
        checkin_btn.pack(side="left")

    def highlight_selected(self):
        """Highlight selected item"""
        self.display_kit_items()

    def checkout_item(self, item):
        """Check out an item from kit"""
        if item["stock"] > 0:
            item["stock"] -= 1
            self.display_kit_items()

    def checkin_item(self, item):
        """Check in an item to kit"""
        if item["stock"] < item["quantity"]:
            item["stock"] += 1
            self.display_kit_items()

    def update_completion(self):
        """Update completion percentage"""
        if not self.kit_items:
            percentage = 0
        else:
            total_quantity = sum(item["quantity"] for item in self.kit_items)
            total_stock = sum(item["stock"] for item in self.kit_items)
            percentage = (total_stock / total_quantity * 100) if total_quantity > 0 else 0

        self.completion_label.configure(text=f"Completion: {int(percentage)}%")
        self.completion_bar.set(percentage / 100)

    def open_add_item_dialog(self):
        """Open dialog to add new item"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Item to First Aid Kit")
        dialog.geometry("400x400")
        dialog.configure(fg_color=self.colors["bg_primary"])

        # Name
        name_label = ctk.CTkLabel(
            dialog,
            text="Item Name:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        name_label.pack(anchor="w", padx=20, pady=(20, 5))

        name_entry = ctk.CTkEntry(dialog, placeholder_text="e.g., Adhesive Bandages")
        name_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Category
        category_label = ctk.CTkLabel(
            dialog,
            text="Category:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        category_label.pack(anchor="w", padx=20, pady=(0, 5))

        category_var = ctk.StringVar(value="Wound Care")
        category_combo = ctk.CTkComboBox(
            dialog,
            values=["Wound Care", "Medication", "Equipment", "Tools", "Other"],
            variable=category_var,
            state="readonly"
        )
        category_combo.pack(fill="x", padx=20, pady=(0, 15))

        # Quantity
        quantity_label = ctk.CTkLabel(
            dialog,
            text="Total Quantity:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        quantity_label.pack(anchor="w", padx=20, pady=(0, 5))

        quantity_entry = ctk.CTkEntry(dialog, placeholder_text="0")
        quantity_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        def save_item():
            name = name_entry.get()
            category = category_var.get()
            quantity = int(quantity_entry.get()) if quantity_entry.get().isdigit() else 0

            if name and quantity > 0:
                new_item = {
                    "id": max([item.get("id", 0) for item in self.kit_items], default=0) + 1,
                    "name": name,
                    "category": category,
                    "quantity": quantity,
                    "stock": quantity,
                    "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                    "status": "Good"
                }
                self.kit_items.append(new_item)
                self.display_kit_items()
                dialog.destroy()

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=save_item,
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

    def edit_selected_item(self):
        """Edit selected item"""
        if not self.selected_item:
            return

        # Similar to add_item_dialog but with existing values
        self.open_add_item_dialog()

    def delete_selected_item(self):
        """Delete selected item"""
        if self.selected_item and self.selected_item in self.kit_items:
            self.kit_items.remove(self.selected_item)
            self.selected_item = None
            self.display_kit_items()
