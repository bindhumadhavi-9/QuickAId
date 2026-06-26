"""
Voice Assistant Module
Voice features using pyttsx3 for reading treatment instructions
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card
import threading

# Try to import pyttsx3, fallback if not available
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class VoiceAssistantPage(ctk.CTkFrame):
    """Voice Assistant page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.is_speaking = False
        self.current_text = ""

        # Initialize text-to-speech engine if available
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)  # Speed of speech
                self.tts_engine.setProperty('volume', 0.9)  # Volume
            except:
                self.tts_engine = None
        else:
            self.tts_engine = None

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_controls()
        self.create_content_area()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Voice Assistant",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Listen to health instructions and guidance read aloud",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_controls(self):
        """Create control buttons"""
        control_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        control_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        # Status indicator
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="Ready",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["success"]
        )
        self.status_label.pack(side="left", padx=20, pady=15)

        # Voice speed control
        speed_label = ctk.CTkLabel(
            control_frame,
            text="Speed:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        speed_label.pack(side="left", padx=(20, 10))

        self.speed_slider = ctk.CTkSlider(
            control_frame,
            from_=50,
            to=250,
            number_of_steps=20,
            command=self.on_speed_change,
            height=4,
            width=150
        )
        self.speed_slider.set(150)
        self.speed_slider.pack(side="left", padx=10)

        # Volume control
        volume_label = ctk.CTkLabel(
            control_frame,
            text="Volume:",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        volume_label.pack(side="left", padx=(20, 10))

        self.volume_slider = ctk.CTkSlider(
            control_frame,
            from_=0,
            to=1,
            number_of_steps=10,
            command=self.on_volume_change,
            height=4,
            width=150
        )
        self.volume_slider.set(0.9)
        self.volume_slider.pack(side="left", padx=10)

        # Stop button
        stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹ Stop",
            command=self.stop_speaking,
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        stop_btn.pack(side="right", padx=20, pady=15)

    def create_content_area(self):
        """Create content area"""
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)

        # Voice assistant status
        status_card = create_card(container)
        status_card.pack(fill="x", pady=10)

        status_frame = ctk.CTkFrame(status_card, fg_color="transparent")
        status_frame.pack(fill="both", expand=True, padx=20, pady=15)

        if PYTTSX3_AVAILABLE and self.tts_engine:
            status_text = "Voice Assistant is enabled. Click any 'Speak' button to listen to health information."
            status_color = self.colors["success"]
        else:
            status_text = "Text-to-speech is not available. Please install pyttsx3 to enable voice features."
            status_color = self.colors["warning"]

        status_check = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=status_color,
            justify="left",
            wraplength=500
        )
        status_check.pack(anchor="w")

        # Available guidance
        title = ctk.CTkLabel(
            container,
            text="Available Health Guidance",
            font=ctk.CTkFont(size=18, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(20, 15))

        guidance_items = [
            {
                "title": "CPR Instructions",
                "text": "Cardiopulmonary Resuscitation. Call emergency services first. Place the person on their back. Position yourself at their side. Place the heel of one hand on the center of the chest, then place your other hand on top. Push hard and fast at least 2 inches deep at a rate of 100 to 120 compressions per minute. Continue until emergency help arrives or the person shows signs of life."
            },
            {
                "title": "Recovery Position",
                "text": "For an unconscious person who is breathing. Kneel beside the person. Straighten both legs. Place one arm across their chest. Bend their near leg at the knee. Roll the person toward you using the bent leg. Tilt their head back to keep the airway open. Monitor their breathing and pulse while waiting for emergency help."
            },
            {
                "title": "Choking Relief",
                "text": "Ask the person if they are choking. For an adult, perform the Heimlich maneuver. Stand behind the person. Place your hands around their waist. Make a fist and place it above the navel, below the rib cage. Press hard into the abdomen. Repeat until the object is dislodged or help arrives. For infants, use back blows and chest thrusts instead."
            },
            {
                "title": "Severe Bleeding Control",
                "text": "Call emergency services immediately. Do not remove embedded objects. Apply direct pressure to the wound with a clean cloth. Maintain pressure for at least 10 minutes. If blood soaks through, add more cloth on top, do not remove the first one. Elevate the injured area above the heart if possible. Apply a tourniquet above the wound if bleeding cannot be controlled."
            },
            {
                "title": "Burn Treatment",
                "text": "Remove the person from the heat source. For minor burns, cool the affected area with cool running water for 10 to 20 minutes. Do not use ice directly on the skin. Remove any tight items like rings or bracelets. Do not apply ointments or ice directly. Cover with a clean, dry cloth. Take pain reliever if needed. Seek medical attention for serious burns."
            },
            {
                "title": "Fracture Care",
                "text": "Immobilize the injured area. Do not try to straighten the fracture. Apply ice wrapped in cloth for 15 to 20 minutes, several times a day. Elevate if possible. Use a sling or splint to support the injury. Do not move the injured limb unnecessarily. Seek medical attention promptly."
            },
        ]

        for item in guidance_items:
            self.create_guidance_card(container, item)

    def create_guidance_card(self, parent, item):
        """Create a guidance card with speak button"""
        card = create_card(parent)
        card.pack(fill="x", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(
            header,
            text=item["title"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(side="left", anchor="w")

        speak_btn = ctk.CTkButton(
            header,
            text="🔊 Speak",
            command=lambda t=item["text"]: self.speak_text(t),
            fg_color=self.colors["info"],
            hover_color="#0284c7",
            text_color="#ffffff",
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            height=28,
            width=80,
            corner_radius=6
        )
        speak_btn.pack(side="right")

        # Content
        content = ctk.CTkLabel(
            frame,
            text=item["text"],
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=500
        )
        content.pack(anchor="w")

    def speak_text(self, text):
        """Speak the provided text"""
        if not self.tts_engine:
            return

        self.is_speaking = True
        self.current_text = text
        self.status_label.configure(text="Speaking...", text_color=self.colors["info"])

        # Run in separate thread to avoid blocking UI
        def speak_thread():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
            finally:
                self.is_speaking = False
                self.status_label.configure(text="Ready", text_color=self.colors["success"])

        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()

    def stop_speaking(self):
        """Stop speaking"""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
            except:
                pass
            self.is_speaking = False
            self.status_label.configure(text="Stopped", text_color=self.colors["warning"])

    def on_speed_change(self, value):
        """Handle speed change"""
        if self.tts_engine:
            self.tts_engine.setProperty('rate', int(value))

    def on_volume_change(self, value):
        """Handle volume change"""
        if self.tts_engine:
            self.tts_engine.setProperty('volume', float(value))
