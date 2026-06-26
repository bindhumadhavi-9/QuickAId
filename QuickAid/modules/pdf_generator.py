"""
PDF Generator Module
PDF report generation using reportlab for symptom results, quiz results, kit status
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card
from datetime import datetime
import os

# Try to import reportlab
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFGeneratorPage(ctk.CTkFrame):
    """PDF Generator page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_info_banner()
        self.create_content_area()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="PDF Report Generator",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Generate and download PDF reports of your health data",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_info_banner(self):
        """Create information banner"""
        info_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"])
        info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        if REPORTLAB_AVAILABLE:
            info_text = "PDF generation is enabled. You can download reports in PDF format."
            info_color = self.colors["success"]
        else:
            info_text = "PDF generation requires reportlab. Please install it to enable PDF export: pip install reportlab"
            info_color = self.colors["warning"]

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=info_color
        )
        info_label.pack(padx=20, pady=15)

    def create_content_area(self):
        """Create content area"""
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)

        # Symptom Checker Report
        self.create_report_section(
            container,
            "Symptom Checker Report",
            "Generate a PDF report of your symptom assessment results with recommendations",
            self.generate_symptom_report,
            "📋 Generate Symptom Report"
        )

        # Quiz Results Report
        self.create_report_section(
            container,
            "Quiz Results Report",
            "Export your learning quiz results and scores to PDF",
            self.generate_quiz_report,
            "🎓 Generate Quiz Report"
        )

        # First Aid Kit Status Report
        self.create_report_section(
            container,
            "First Aid Kit Status Report",
            "Create a detailed report of your first aid kit inventory and status",
            self.generate_kit_report,
            "🏥 Generate Kit Report"
        )

        # Health Tools Summary Report
        self.create_report_section(
            container,
            "Health Tools Summary Report",
            "Generate a report with your health measurements and calculations",
            self.generate_health_tools_report,
            "📊 Generate Health Report"
        )

        # Emergency Contacts Report
        self.create_report_section(
            container,
            "Emergency Contacts Report",
            "Export your emergency contacts list to PDF format",
            self.generate_contacts_report,
            "📞 Generate Contacts Report"
        )

    def create_report_section(self, parent, title, description, command, button_text):
        """Create a report generation section"""
        card = create_card(parent)
        card.pack(fill="x", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Title
        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title_label.pack(anchor="w", pady=(0, 8))

        # Description
        desc_label = ctk.CTkLabel(
            frame,
            text=description,
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=500
        )
        desc_label.pack(anchor="w", pady=(0, 12))

        # Button frame
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(anchor="w", fill="x", pady=(5, 0))

        generate_btn = ctk.CTkButton(
            button_frame,
            text=button_text,
            command=command,
            fg_color=self.colors["success"],
            hover_color="#059669",
            text_color="#ffffff",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            height=32,
            corner_radius=6
        )
        generate_btn.pack(side="left")

        # Status label
        status_label = ctk.CTkLabel(
            button_frame,
            text="",
            font=ctk.CTkFont(size=10, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        status_label.pack(side="left", padx=15)

    def generate_symptom_report(self):
        """Generate symptom checker report"""
        if not REPORTLAB_AVAILABLE:
            self.show_error("reportlab not installed")
            return

        try:
            filename = f"QuickAid_Symptom_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.expanduser(f"~/Downloads/{filename}")

            # Create PDF
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#e94560'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Symptom Checker Report", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Date
            date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Sample data
            story.append(Paragraph("Selected Symptoms:", styles['Heading2']))
            symptoms = ["Fever", "Cough", "Sore Throat"]
            for symptom in symptoms:
                story.append(Paragraph(f"• {symptom}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            story.append(Paragraph("Possible Conditions:", styles['Heading2']))
            conditions = ["Cold/Flu", "COVID-19", "Bronchitis"]
            for condition in conditions:
                story.append(Paragraph(f"• {condition}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            story.append(Paragraph("Recommendations:", styles['Heading2']))
            recommendations = [
                "Rest and get adequate sleep (7-9 hours)",
                "Stay hydrated - drink plenty of water",
                "Consult a healthcare provider if symptoms persist"
            ]
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", styles['Normal']))

            # Build PDF
            doc.build(story)
            self.show_success(f"Report saved to {filepath}")

        except Exception as e:
            self.show_error(f"Error generating report: {str(e)}")

    def generate_quiz_report(self):
        """Generate quiz results report"""
        if not REPORTLAB_AVAILABLE:
            self.show_error("reportlab not installed")
            return

        try:
            filename = f"QuickAid_Quiz_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.expanduser(f"~/Downloads/{filename}")

            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#10b981'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Quiz Results Report", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Date
            date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Quiz results
            story.append(Paragraph("Quiz: First Aid Basics Quiz", styles['Heading2']))
            story.append(Paragraph("Score: 8/10 (80%)", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("Performance: Excellent", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            story.append(Paragraph("Questions Answered:", styles['Heading3']))
            questions = [
                "What should you do first in case of severe bleeding? - Correct",
                "What is the correct CPR compression rate? - Correct",
                "For how long should you apply heat to a sprain? - Incorrect"
            ]
            for q in questions:
                story.append(Paragraph(f"• {q}", styles['Normal']))

            # Build PDF
            doc.build(story)
            self.show_success(f"Report saved to {filepath}")

        except Exception as e:
            self.show_error(f"Error generating report: {str(e)}")

    def generate_kit_report(self):
        """Generate kit status report"""
        if not REPORTLAB_AVAILABLE:
            self.show_error("reportlab not installed")
            return

        try:
            filename = f"QuickAid_Kit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.expanduser(f"~/Downloads/{filename}")

            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#3b82f6'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("First Aid Kit Status Report", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Date
            date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Kit summary
            story.append(Paragraph("Kit Summary:", styles['Heading2']))
            story.append(Paragraph("Total Items: 5", styles['Normal']))
            story.append(Paragraph("Completion: 88%", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            # Items table
            story.append(Paragraph("Inventory:", styles['Heading2']))
            data = [
                ['Item', 'Category', 'Stock', 'Status'],
                ['Adhesive Bandages', 'Wound Care', '40/50', 'Good'],
                ['Gauze Pads', 'Wound Care', '18/20', 'Good'],
                ['Pain Relief Tablets', 'Medication', '22/30', 'Good'],
            ]
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

            # Build PDF
            doc.build(story)
            self.show_success(f"Report saved to {filepath}")

        except Exception as e:
            self.show_error(f"Error generating report: {str(e)}")

    def generate_health_tools_report(self):
        """Generate health tools summary report"""
        if not REPORTLAB_AVAILABLE:
            self.show_error("reportlab not installed")
            return

        try:
            filename = f"QuickAid_Health_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.expanduser(f"~/Downloads/{filename}")

            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#f59e0b'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Health Tools Summary Report", title_style))
            story.append(Spacer(1, 0.2*inch))

            # BMI
            story.append(Paragraph("BMI Calculator Results:", styles['Heading2']))
            story.append(Paragraph("Weight: 70 kg | Height: 175 cm", styles['Normal']))
            story.append(Paragraph("BMI: 22.9 (Normal Weight)", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            # Water intake
            story.append(Paragraph("Water Intake Calculator:", styles['Heading2']))
            story.append(Paragraph("Recommended Daily Intake: 2.1 L", styles['Normal']))
            story.append(Paragraph("Approximately 8-9 glasses per day", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            # Calories
            story.append(Paragraph("Daily Calorie Estimator:", styles['Heading2']))
            story.append(Paragraph("Maintenance: 2100 calories/day", styles['Normal']))
            story.append(Paragraph("Weight Loss: 1700 calories/day", styles['Normal']))
            story.append(Paragraph("Weight Gain: 2500 calories/day", styles['Normal']))

            # Build PDF
            doc.build(story)
            self.show_success(f"Report saved to {filepath}")

        except Exception as e:
            self.show_error(f"Error generating report: {str(e)}")

    def generate_contacts_report(self):
        """Generate emergency contacts report"""
        if not REPORTLAB_AVAILABLE:
            self.show_error("reportlab not installed")
            return

        try:
            filename = f"QuickAid_Contacts_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.expanduser(f"~/Downloads/{filename}")

            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#ef4444'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Emergency Contacts Report", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Contacts table
            data = [
                ['Name', 'Category', 'Phone', 'Email'],
                ['Mom', 'Family', '+91-9876543210', 'mom@email.com'],
                ['Dr. Singh', 'Doctors', '+91-9876543212', 'dr.singh@clinic.com'],
                ['City Hospital', 'Hospitals', '+91-9876543213', 'info@cityhospital.com'],
            ]
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

            # Build PDF
            doc.build(story)
            self.show_success(f"Report saved to {filepath}")

        except Exception as e:
            self.show_error(f"Error generating report: {str(e)}")

    def show_success(self, message):
        """Show success message"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success")
        dialog.geometry("300x150")
        dialog.configure(fg_color=self.colors["bg_primary"])

        label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["success"],
            justify="center",
            wraplength=250
        )
        label.pack(expand=True, padx=20, pady=20)

        btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            fg_color=self.colors["success"],
            hover_color="#059669",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold")
        )
        btn.pack(pady=10)

    def show_error(self, message):
        """Show error message"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("300x150")
        dialog.configure(fg_color=self.colors["bg_primary"])

        label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["danger"],
            justify="center",
            wraplength=250
        )
        label.pack(expand=True, padx=20, pady=20)

        btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            fg_color=self.colors["danger"],
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold")
        )
        btn.pack(pady=10)
