"""
Interactive Human Body System Module
Clickable body parts with first aid information
"""

import customtkinter as ctk
from tkinter import messagebox
import json
from gui.themes import ThemeManager, create_card


class BodySystemPage(ctk.CTkFrame):
    """Interactive body system page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.gender = "male"
        self.view = "front"

        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.create_controls()
        self.create_body_view()
        self.create_info_panel()

    def create_controls(self):
        """Create control panel"""
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        control_frame.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(
            control_frame,
            text="Interactive Body Map",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.grid(row=0, column=0, pady=20)

        # Gender selection
        gender_label = ctk.CTkLabel(
            control_frame,
            text="Select Gender:",
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        gender_label.grid(row=1, column=0, pady=10)

        gender_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        gender_frame.grid(row=2, column=0, pady=5)

        self.male_btn = ctk.CTkButton(
            gender_frame,
            text="Male",
            width=80,
            fg_color=self.colors["accent"],
            command=lambda: self.set_gender("male")
        )
        self.male_btn.pack(side="left", padx=5)

        self.female_btn = ctk.CTkButton(
            gender_frame,
            text="Female",
            width=80,
            fg_color="transparent",
            border_width=2,
            border_color=self.colors["border"],
            text_color=self.colors["text_primary"],
            command=lambda: self.set_gender("female")
        )
        self.female_btn.pack(side="left", padx=5)

        # View selection
        view_label = ctk.CTkLabel(
            control_frame,
            text="Select View:",
            font=ctk.CTkFont(size=14, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        view_label.grid(row=3, column=0, pady=(20, 10))

        view_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        view_frame.grid(row=4, column=0, pady=5)

        self.front_btn = ctk.CTkButton(
            view_frame,
            text="Front",
            width=80,
            fg_color=self.colors["accent"],
            command=lambda: self.set_view("front")
        )
        self.front_btn.pack(side="left", padx=5)

        self.back_btn = ctk.CTkButton(
            view_frame,
            text="Back",
            width=80,
            fg_color="transparent",
            border_width=2,
            border_color=self.colors["border"],
            text_color=self.colors["text_primary"],
            command=lambda: self.set_view("back")
        )
        self.back_btn.pack(side="left", padx=5)

        # Instructions
        instructions = ctk.CTkLabel(
            control_frame,
            text="Click on a body part\nfor first aid information",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="center"
        )
        instructions.grid(row=5, column=0, pady=30)

        # Body parts list
        parts_label = ctk.CTkLabel(
            control_frame,
            text="Body Parts:",
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        parts_label.grid(row=6, column=0, pady=(10, 5))

        # Scrollable frame for body parts
        parts_frame = ctk.CTkScrollableFrame(control_frame, height=300)
        parts_frame.grid(row=7, column=0, sticky="nsew", pady=5)

        body_parts = ["Head", "Eyes", "Ears", "Nose", "Mouth", "Neck", "Shoulders",
                      "Chest", "Back", "Arms", "Elbows", "Hands", "Fingers",
                      "Abdomen", "Waist", "Hips", "Thighs", "Knees", "Legs",
                      "Ankles", "Feet"]

        for part in body_parts:
            btn = ctk.CTkButton(
                parts_frame,
                text=part,
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                fg_color="transparent",
                text_color=self.colors["text_primary"],
                hover_color=self.colors["bg_tertiary"],
                anchor="w",
                height=30,
                command=lambda p=part: self.show_body_part_info(p.lower())
            )
            btn.pack(fill="x", pady=2, padx=5)

    def create_body_view(self):
        """Create interactive body view"""
        body_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["card_bg"],
            corner_radius=15
        )
        body_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        body_frame.grid_columnconfigure(0, weight=1)
        body_frame.grid_rowconfigure(0, weight=1)

        # Body canvas placeholder
        self.body_canvas = BodyCanvas(body_frame, self.colors, self.on_body_part_click)
        self.body_canvas.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def create_info_panel(self):
        """Create information panel"""
        info_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["card_bg"],
            corner_radius=15
        )
        info_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Placeholder text
        self.info_placeholder = ctk.CTkLabel(
            info_frame,
            text="Select a body part to view\nfirst aid information",
            font=ctk.CTkFont(size=16, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="center"
        )
        self.info_placeholder.pack(pady=50)

        # Info content frame (hidden initially)
        self.info_content = ctk.CTkFrame(info_frame, fg_color="transparent")

        # Title
        self.part_title = ctk.CTkLabel(
            self.info_content,
            text="",
            font=ctk.CTkFont(size=22, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        self.part_title.pack(pady=10)

        # Tab view
        self.tabview = ctk.CTkTabview(self.info_content)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.injuries_tab = self.tabview.add("Injuries")
        self.first_aid_tab = self.tabview.add("First Aid")
        self.warnings_tab = self.tabview.add("Warnings")
        self.prevention_tab = self.tabview.add("Prevention")

    def set_gender(self, gender):
        """Set body gender"""
        self.gender = gender
        if gender == "male":
            self.male_btn.configure(fg_color=self.colors["accent"])
            self.female_btn.configure(fg_color="transparent", border_width=2)
        else:
            self.female_btn.configure(fg_color=self.colors["accent"])
            self.male_btn.configure(fg_color="transparent", border_width=2)
        self.body_canvas.set_gender(gender)

    def set_view(self, view):
        """Set body view (front/back)"""
        self.view = view
        if view == "front":
            self.front_btn.configure(fg_color=self.colors["accent"])
            self.back_btn.configure(fg_color="transparent", border_width=2)
        else:
            self.back_btn.configure(fg_color=self.colors["accent"])
            self.front_btn.configure(fg_color="transparent", border_width=2)
        self.body_canvas.set_view(view)

    def on_body_part_click(self, part_name):
        """Handle body part click"""
        self.show_body_part_info(part_name)

    def show_body_part_info(self, part_name):
        """Show information for selected body part"""
        # Fetch data from database
        part_data = self.db.fetchone(
            "SELECT * FROM body_parts WHERE part_name = ?",
            (part_name.capitalize(),)
        )

        if not part_data:
            # Try lowercase
            part_data = self.db.fetchone(
                "SELECT * FROM body_parts WHERE part_name = ?",
                (part_name,)
            )

        if part_data:
            self.info_placeholder.pack_forget()
            self.info_content.pack(fill="both", expand=True, pady=20)

            # Update title
            self.part_title.configure(text=part_data["part_name"])

            # Update tabs
            self.update_tab(self.injuries_tab, part_data, "injuries")
            self.update_tab(self.first_aid_tab, part_data, "first_aid")
            self.update_tab(self.warnings_tab, part_data, "warnings")
            self.update_tab(self.prevention_tab, part_data, "prevention")

    def update_tab(self, tab, data, tab_type):
        """Update tab content"""
        # Clear existing widgets
        for widget in tab.winfo_children():
            widget.destroy()

        if tab_type == "injuries":
            content = f"Common Injuries:\n\n{self.format_json(data['common_injuries'])}\n\n"
            content += f"Causes:\n\n{self.format_json(data['causes'])}\n\n"
            content += f"Symptoms:\n\n{self.format_json(data['symptoms'])}"
        elif tab_type == "first_aid":
            content = f"First Aid Treatment:\n\n{self.format_json(data['first_aid'])}\n\n"
            content += f"Do's:\n\n{self.format_json(data['dos'])}\n\n"
            content += f"Don'ts:\n\n{self.format_json(data['donts'])}\n\n"
            content += f"Recovery Tips:\n\n{self.format_json(data['recovery_tips'])}"
        elif tab_type == "warnings":
            content = f"Emergency Warning Signs:\n\n{self.format_json(data['warning_signs'])}\n\n"
            content += f"When to See Doctor:\n\n{data['doctor_advice']}\n\n"
            content += f"Recommended Medicines:\n\n{self.format_json(data['medicines'])}"
        else:
            content = f"Prevention Methods:\n\n{self.format_json(data['prevention'])}"

        label = ctk.CTkLabel(
            tab,
            text=content,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=350
        )
        label.pack(padx=10, pady=10, anchor="nw")

    def format_json(self, json_str):
        """Format JSON string to readable text"""
        try:
            items = json.loads(json_str)
            if isinstance(items, list):
                return "\n".join([f"• {item}" for item in items])
            return str(items)
        except:
            return json_str


class BodyCanvas(ctk.CTkCanvas):
    """Custom canvas for interactive body drawing"""

    def __init__(self, parent, colors, click_callback):
        super().__init__(parent, bg=colors["card_bg"], highlightthickness=0)
        self.colors = colors
        self.click_callback = click_callback
        self.gender = "male"
        self.view = "front"
        self.body_parts = {}
        self.bind("<Configure>", self.on_resize)
        self.bind("<Motion>", self.on_motion)

    def set_gender(self, gender):
        """Set body gender"""
        self.gender = gender
        self.draw_body()

    def set_view(self, view):
        """Set body view"""
        self.view = view
        self.draw_body()

    def on_resize(self, event):
        """Handle resize"""
        self.draw_body()

    def on_motion(self, event):
        """Handle mouse motion for hover effects"""
        self.check_hover(event.x, event.y)

    def draw_body(self):
        """Draw the human body"""
        self.delete("all")

        w = self.winfo_width()
        h = self.winfo_height()
        cx = w // 2

        if w < 50 or h < 50:
            return

        # Calculate proportions
        scale = min(w, h) / 600

        # Colors
        body_color = self.colors["bg_tertiary"]
        hover_color = self.colors["accent"]

        # Body regions with clickable areas
        # Using simplified geometric shapes

        # Head (circle)
        head_r = int(50 * scale)
        self.create_oval(
            cx - head_r, int(30 * scale),
            cx + head_r, int(30 * scale) + head_r * 2,
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "head")
        )
        self.body_parts["head"] = (cx - head_r, int(30 * scale), cx + head_r, int(30 * scale) + head_r * 2)

        # Neck (rectangle)
        self.create_rectangle(
            cx - int(20 * scale), int(130 * scale),
            cx + int(20 * scale), int(160 * scale),
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "neck")
        )

        # Torso - Chest/Abdomen
        body_width = int(100 * scale)
        if self.gender == "male":
            # Broader shoulders
            self.create_polygon(
                cx - body_width, int(160 * scale),
                cx + body_width, int(160 * scale),
                cx + int(80 * scale), int(320 * scale),
                cx - int(80 * scale), int(320 * scale),
                fill=body_color, outline=hover_color, width=2,
                tags=("body_part", "chest")
            )
        else:
            # Female shape
            self.create_polygon(
                cx - body_width, int(160 * scale),
                cx + body_width, int(160 * scale),
                cx + int(90 * scale), int(280 * scale),
                cx - int(90 * scale), int(280 * scale),
                fill=body_color, outline=hover_color, width=2,
                tags=("body_part", "chest")
            )

        # Abdomen
        self.create_polygon(
            cx - int(80 * scale), int(320 * scale),
            cx + int(80 * scale), int(320 * scale),
            cx + int(70 * scale), int(420 * scale),
            cx - int(70 * scale), int(420 * scale),
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "abdomen")
        )

        # Arms
        arm_width = int(30 * scale)

        # Left arm
        self.create_polYgon = [
            cx - body_width, int(160 * scale),
            cx - body_width - arm_width, int(170 * scale),
            cx - body_width - arm_width - int(10 * scale), int(280 * scale),
            cx - body_width - arm_width + int(10 * scale), int(280 * scale),
            cx - body_width + int(20 * scale), int(160 * scale),
        ]
        self.create_polygon(
            cx - body_width - arm_width - int(10 * scale), int(170 * scale),
            cx - body_width, int(160 * scale),
            cx - body_width + int(20 * scale), int(160 * scale),
            cx - body_width + int(15 * scale) - int(30 * scale), int(290 * scale),
            cx - body_width - arm_width - int(20 * scale), int(290 * scale),
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "arms")
        )

        # Right arm
        self.create_polygon(
            cx + body_width + arm_width + int(10 * scale), int(170 * scale),
            cx + body_width, int(160 * scale),
            cx + body_width - int(20 * scale), int(160 * scale),
            cx + body_width - int(15 * scale) + int(30 * scale), int(290 * scale),
            cx + body_width + arm_width + int(20 * scale), int(290 * scale),
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "arms")
        )

        # Hands
        hand_r = int(25 * scale)
        self.create_oval(
            cx - body_width - arm_width - int(20 * scale) - hand_r,
            int(290 * scale),
            cx - body_width - arm_width - int(20 * scale) + hand_r,
            int(290 * scale) + hand_r * 2,
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "hands")
        )
        self.create_oval(
            cx + body_width + arm_width + int(20 * scale) - hand_r,
            int(290 * scale),
            cx + body_width + arm_width + int(20 * scale) + hand_r,
            int(290 * scale) + hand_r * 2,
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "hands")
        )

        # Legs
        leg_width = int(40 * scale)

        # Left leg
        self.create_polygon(
            cx - int(70 * scale), int(420 * scale),
            cx - int(20 * scale), int(420 * scale),
            cx - int(25 * scale), int(550 * scale),
            cx - int(65 * scale), int(550 * scale),
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "legs")
        )

        # Right leg
        self.create_polygon(
            cx + int(20 * scale), int(420 * scale),
            cx + int(70 * scale), int(420 * scale),
            cx + int(65 * scale), int(550 * scale),
            cx + int(25 * scale), int(550 * scale),
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "legs")
        )

        # Feet
        foot_w = int(40 * scale)
        foot_h = int(20 * scale)
        self.create_oval(
            cx - int(65 * scale) - foot_w, int(550 * scale),
            cx - int(25 * scale) + foot_w, int(550 * scale) + foot_h * 2,
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "feet")
        )
        self.create_oval(
            cx + int(25 * scale) - foot_w, int(550 * scale),
            cx + int(65 * scale) + foot_w, int(550 * scale) + foot_h * 2,
            fill=body_color, outline=hover_color, width=2,
            tags=("body_part", "feet")
        )

        # Labels
        if self.view == "front":
            self.create_text(cx, int(60 * scale), text="Head", fill=self.colors["text_primary"], font=("Segoe UI", 10))
            self.create_text(cx, int(240 * scale), text="Chest", fill=self.colors["text_primary"], font=("Segoe UI", 10))
            self.create_text(cx, int(370 * scale), text="Abdomen", fill=self.colors["text_primary"], font=("Segoe UI", 10))
            self.create_text(cx - int(130 * scale), int(220 * scale), text="Arm", fill=self.colors["text_primary"], font=("Segoe UI", 9))
            self.create_text(cx + int(130 * scale), int(220 * scale), text="Arm", fill=self.colors["text_primary"], font=("Segoe UI", 9))
            self.create_text(cx - int(45 * scale), int(480 * scale), text="Leg", fill=self.colors["text_primary"], font=("Segoe UI", 9))
            self.create_text(cx + int(45 * scale), int(480 * scale), text="Leg", fill=self.colors["text_primary"], font=("Segoe UI", 9))

        # Bind clicks
        self.tag_bind("body_part", "<Button-1>", self.on_click)

    def on_click(self, event):
        """Handle click on body part"""
        # Find the tag of the clicked item
        tags = self.gettags(self.find_closest(event.x, event.y)[0])
        if tags and len(tags) > 1:
            part_name = tags[1]
            if part_name in ["head", "chest", "abdomen", "arms", "hands", "legs", "feet", "neck"]:
                self.click_callback(part_name)

    def check_hover(self, x, y):
        """Check for hover effects"""
        items = self.find_overlapping(x - 5, y - 5, x + 5, y + 5)
        if items:
            self.config(cursor="hand2")
        else:
            self.config(cursor="")
