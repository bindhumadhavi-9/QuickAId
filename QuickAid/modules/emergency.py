"""
Emergency Module
Large SOS screen with emergency numbers and emergency instructions
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class EmergencyPage(ctk.CTkFrame):
    """Emergency SOS page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.sos_active = False

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_emergency_screen()

    def create_emergency_screen(self):
        """Create emergency SOS screen"""
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)

        # SOS Button - Large Red Button
        sos_frame = create_card(container)
        sos_frame.pack(fill="x", pady=20)

        sos_button = ctk.CTkButton(
            sos_frame,
            text="🆘 SOS\nTap to Activate",
            command=self.toggle_sos,
            font=ctk.CTkFont(size=48, family="Segoe UI", weight="bold"),
            fg_color=self.colors["danger"],
            hover_color="#991b1b",
            text_color="#ffffff",
            corner_radius=20,
            height=200,
            border_width=3,
            border_color="#ffcccc"
        )
        sos_button.pack(fill="both", expand=True, padx=20, pady=20)

        self.sos_status_label = ctk.CTkLabel(
            sos_frame,
            text="Press the SOS button in case of emergency",
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        self.sos_status_label.pack(pady=(0, 20))

        # Emergency Numbers
        numbers_title = ctk.CTkLabel(
            container,
            text="Emergency Numbers",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        numbers_title.pack(anchor="w", pady=(20, 15))

        emergency_numbers = [
            {"number": "112", "service": "Police", "color": "#2563eb"},
            {"number": "108", "service": "Ambulance/Medical", "color": "#ef4444"},
            {"number": "100", "service": "Fire Department", "color": "#f59e0b"},
            {"number": "101", "service": "Fire Emergency", "color": "#f97316"},
            {"number": "1091", "service": "Women's Helpline", "color": "#a855f7"},
            {"number": "1098", "service": "Child Helpline", "color": "#06b6d4"},
        ]

        for item in emergency_numbers:
            self.create_emergency_number_card(container, item)

        # Emergency Instructions
        instructions_title = ctk.CTkLabel(
            container,
            text="What to Do in an Emergency",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        instructions_title.pack(anchor="w", pady=(20, 15))

        instructions = [
            {
                "title": "Stay Calm",
                "description": "Take deep breaths and try to remain calm. Panic can affect your judgment.",
                "icon": "🧘"
            },
            {
                "title": "Assess the Situation",
                "description": "Quickly evaluate what happened and if anyone is in immediate danger.",
                "icon": "👁"
            },
            {
                "title": "Call for Help",
                "description": "Dial emergency number (112) and provide clear information about the situation.",
                "icon": "📞"
            },
            {
                "title": "Provide First Aid",
                "description": "If trained, provide basic first aid while waiting for emergency services.",
                "icon": "🏥"
            },
            {
                "title": "Move to Safety",
                "description": "If safe to do so, move to a safer location and away from danger.",
                "icon": "🚨"
            },
            {
                "title": "Wait for Help",
                "description": "Stay at the location or follow dispatcher instructions. Do not move the injured person unnecessarily.",
                "icon": "⏳"
            },
        ]

        instructions_container = ctk.CTkFrame(container, fg_color="transparent")
        instructions_container.pack(fill="x", pady=10)

        for i, instruction in enumerate(instructions):
            col = i % 2
            row = i // 2

            if col == 0:
                row_frame = ctk.CTkFrame(instructions_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=10)

            self.create_instruction_card(row_frame if col == 0 else row_frame, instruction)

        # Important Information Box
        info_title = ctk.CTkLabel(
            container,
            text="Important Information",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        info_title.pack(anchor="w", pady=(20, 15))

        info_card = create_card(container)
        info_card.pack(fill="x", pady=10)

        info_text = """When calling emergency services:

1. Stay on the line until they hang up
2. Provide your location clearly (address/landmarks)
3. Describe the situation briefly
4. Mention any injuries or medical conditions
5. Listen to instructions and follow them carefully
6. Keep the person calm while waiting

If you're unsure about the severity, it's better to call. Emergency services can assess and decide."""

        info_label = ctk.CTkLabel(
            info_card,
            text=info_text,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=500
        )
        info_label.pack(anchor="w", padx=20, pady=20)

    def create_emergency_number_card(self, parent, data):
        """Create emergency number card"""
        card = create_card(parent)
        card.pack(fill="x", pady=8)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=15, pady=12)

        # Left side - Number
        number_label = ctk.CTkLabel(
            frame,
            text=data["number"],
            font=ctk.CTkFont(size=32, family="Segoe UI", weight="bold"),
            text_color=data["color"]
        )
        number_label.pack(side="left", padx=(0, 20))

        # Middle - Service name
        service_label = ctk.CTkLabel(
            frame,
            text=data["service"],
            font=ctk.CTkFont(size=15, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        service_label.pack(side="left", expand=True, anchor="w")

        # Right side - Call button
        call_btn = ctk.CTkButton(
            frame,
            text="📞 Call",
            command=lambda: self.call_number(data["number"]),
            fg_color=data["color"],
            hover_color=data["color"],
            text_color="#ffffff",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            width=80,
            corner_radius=8
        )
        call_btn.pack(side="right", padx=(10, 0))

    def create_instruction_card(self, parent, instruction):
        """Create instruction card"""
        card = create_card(parent)
        card.pack(side="left", fill="both", expand=True, padx=5)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Icon
        icon_label = ctk.CTkLabel(
            frame,
            text=instruction["icon"],
            font=ctk.CTkFont(size=32, family="Segoe UI"),
            text_color=self.colors["accent"]
        )
        icon_label.pack(pady=(0, 10))

        # Title
        title_label = ctk.CTkLabel(
            frame,
            text=instruction["title"],
            font=ctk.CTkFont(size=13, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title_label.pack(anchor="w", pady=(0, 8))

        # Description
        desc_label = ctk.CTkLabel(
            frame,
            text=instruction["description"],
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=200
        )
        desc_label.pack(anchor="w")

    def toggle_sos(self):
        """Toggle SOS activation"""
        self.sos_active = not self.sos_active

        if self.sos_active:
            self.sos_status_label.configure(
                text="🚨 SOS ACTIVATED - Emergency Services Have Been Notified 🚨",
                text_color=self.colors["danger"]
            )
            # Flash effect
            self.after(500, self.toggle_flash_effect)
        else:
            self.sos_status_label.configure(
                text="Press the SOS button in case of emergency",
                text_color=self.colors["text_secondary"]
            )

    def toggle_flash_effect(self):
        """Flash effect for SOS"""
        if self.sos_active:
            self.after(500, self.toggle_flash_effect)

    def call_number(self, number):
        """Call emergency number"""
        # Placeholder for calling functionality
        pass
