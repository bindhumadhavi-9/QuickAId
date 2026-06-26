"""
Theme Manager for Quick Aid Application
Handles dark/light mode and color schemes
"""

import customtkinter as ctk


class ThemeManager:
    """Manages application themes and colors"""

    # Medical color palette - Dark theme
    DARK_THEME = {
        "bg_primary": "#1a1a2e",
        "bg_secondary": "#16213e",
        "bg_tertiary": "#0f3460",
        "accent": "#e94560",
        "accent_secondary": "#0abbef",
        "text_primary": "#ffffff",
        "text_secondary": "#a0a0a0",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#3b82f6",
        "card_bg": "#1f2940",
        "border": "#2d3748",
        "gradient_start": "#e94560",
        "gradient_end": "#0abbef",
    }

    # Medical color palette - Light theme
    LIGHT_THEME = {
        "bg_primary": "#f8fafc",
        "bg_secondary": "#ffffff",
        "bg_tertiary": "#f1f5f9",
        "accent": "#dc2626",
        "accent_secondary": "#0284c7",
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "info": "#2563eb",
        "card_bg": "#ffffff",
        "border": "#e2e8f0",
        "gradient_start": "#dc2626",
        "gradient_end": "#0284c7",
    }

    MEDICAL_COLORS = {
        # Emergency Red
        "emergency": "#dc2626",
        # Healing Green
        "healing": "#10b981",
        # Medical Blue
        "medical_blue": "#2563eb",
        # Warning Orange
        "warning": "#f59e0b",
        # Care Purple
        "care": "#8b5cf6",
        # Info Cyan
        "info": "#06b6d4",
    }

    def __init__(self):
        self.current_theme = "dark"
        self.colors = self.DARK_THEME.copy()

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.colors = self.LIGHT_THEME.copy()
            ctk.set_appearance_mode("light")
        else:
            self.current_theme = "dark"
            self.colors = self.DARK_THEME.copy()
            ctk.set_appearance_mode("dark")
        return self.colors

    def get_colors(self):
        """Get current theme colors"""
        return self.colors

    def get_theme_name(self):
        """Get current theme name"""
        return self.current_theme


def apply_theme(widget, theme_type="card"):
    """Apply theme styling to a widget"""
    theme_manager = ThemeManager()
    colors = theme_manager.get_colors()

    if theme_type == "card":
        widget.configure(
            fg_color=colors["card_bg"],
            border_width=1,
            border_color=colors["border"]
        )
    elif theme_type == "primary_button":
        widget.configure(
            fg_color=colors["accent"],
            hover_color=colors["emergency"],
            text_color=colors["text_primary"],
            corner_radius=10
        )


def create_styled_label(parent, text, font_size=14, style="primary"):
    """Create a styled CTkLabel"""
    theme_manager = ThemeManager()
    colors = theme_manager.get_colors()

    label = ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=font_size, family="Segoe UI"),
        text_color=colors["text_primary"] if style == "primary" else colors["text_secondary"]
    )
    return label


def create_styled_button(parent, text, command=None, style="primary"):
    """Create a styled CTkButton"""
    theme_manager = ThemeManager()
    colors = theme_manager.get_colors()

    if style == "primary":
        fg_color = colors["accent"]
        hover_color = colors["danger"]
    elif style == "secondary":
        fg_color = colors["bg_tertiary"]
        hover_color = colors["bg_secondary"]
    elif style == "success":
        fg_color = colors["success"]
        hover_color = "#059669"
    elif style == "warning":
        fg_color = colors["warning"]
        hover_color = "#d97706"
    else:
        fg_color = colors["accent_secondary"]
        hover_color = "#0284c7"

    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=fg_color,
        hover_color=hover_color,
        font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
        corner_radius=10,
        height=40
    )
    return button


def create_card(parent, title=None):
    """Create a styled card frame"""
    theme_manager = ThemeManager()
    colors = theme_manager.get_colors()

    card = ctk.CTkFrame(
        parent,
        fg_color=colors["card_bg"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=15
    )
    return card
