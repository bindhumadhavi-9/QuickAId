"""
Learning Center Module
Health articles, first aid tutorials, quiz system with scoring and progress tracking
"""

import customtkinter as ctk
from gui.themes import ThemeManager, create_card


class LearningCenterPage(ctk.CTkFrame):
    """Learning Center page"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.theme = ThemeManager()
        self.colors = self.theme.get_colors()
        self.current_quiz = None
        self.quiz_score = 0
        self.quiz_progress = 0
        self.articles = []
        self.tutorials = []
        self.quizzes = []

        self.configure(fg_color=self.colors["bg_primary"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_tabs()
        self.load_content()

    def create_header(self):
        """Create header section"""
        header = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=100)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Learning Center",
            font=ctk.CTkFont(size=28, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left", padx=20, pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Learn about health, first aid, and take quizzes to test your knowledge",
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        subtitle.pack(side="left", padx=20)

    def create_tabs(self):
        """Create tab buttons"""
        tab_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=50)
        tab_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        self.tab_var = ctk.StringVar(value="articles")

        tabs = [
            ("📰 Articles", "articles"),
            ("🎓 Tutorials", "tutorials"),
            ("❓ Quiz", "quiz")
        ]

        for text, value in tabs:
            btn = ctk.CTkButton(
                tab_frame,
                text=text,
                command=lambda v=value: self.switch_tab(v),
                fg_color="transparent",
                text_color=self.colors["text_primary"],
                hover_color=self.colors["bg_tertiary"],
                font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
                height=40,
                corner_radius=8
            )
            btn.pack(side="left", padx=10, pady=5)

    def create_tabs(self):
        """Create tab buttons"""
        tab_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], height=50)
        tab_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        self.tab_var = ctk.StringVar(value="articles")

        tabs = [
            ("📰 Articles", "articles"),
            ("🎓 Tutorials", "tutorials"),
            ("❓ Quiz", "quiz")
        ]

        for text, value in tabs:
            btn = ctk.CTkButton(
                tab_frame,
                text=text,
                command=lambda v=value: self.switch_tab(v),
                fg_color="transparent",
                text_color=self.colors["text_primary"],
                hover_color=self.colors["bg_tertiary"],
                font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
                height=40,
                corner_radius=8
            )
            btn.pack(side="left", padx=10, pady=5)

        # Create content frame
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg_primary"]
        )
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(2, weight=1)

    def switch_tab(self, tab_name):
        """Switch to different tab"""
        self.tab_var.set(tab_name)

        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if tab_name == "articles":
            self.show_articles()
        elif tab_name == "tutorials":
            self.show_tutorials()
        else:
            self.show_quiz()

    def load_content(self):
        """Load content from database"""
        self.articles = [
            {
                "title": "Understanding Blood Pressure",
                "excerpt": "Learn what blood pressure is, normal ranges, and how to maintain healthy BP...",
                "content": "Blood pressure is the force of blood pushing against blood vessel walls. Normal BP is less than 120/80. High blood pressure (hypertension) increases risk of heart disease and stroke. To maintain healthy BP: exercise regularly, reduce salt intake, manage stress, maintain healthy weight, and monitor your BP regularly.",
                "category": "Health"
            },
            {
                "title": "The Importance of Sleep",
                "excerpt": "Why quality sleep is essential for your physical and mental health...",
                "content": "Quality sleep is crucial for immune function, mental clarity, and overall health. Adults need 7-9 hours per night. Tips for better sleep: maintain consistent sleep schedule, avoid screens 1 hour before bed, keep bedroom cool and dark, limit caffeine, and exercise regularly.",
                "category": "Wellness"
            },
            {
                "title": "Nutrition Basics",
                "excerpt": "Essential nutrients your body needs and where to find them...",
                "content": "A balanced diet includes carbohydrates, proteins, fats, vitamins, and minerals. Each nutrient plays a specific role in maintaining health. Eat plenty of vegetables and fruits, whole grains, lean proteins, and healthy fats. Limit processed foods, added sugars, and salt.",
                "category": "Health"
            },
        ]

        self.tutorials = [
            {
                "title": "CPR Basics",
                "steps": [
                    "Check for responsiveness and breathing",
                    "Call emergency services (112)",
                    "Position the person on their back",
                    "Place heel of one hand on center of chest",
                    "Push hard and fast at least 2 inches deep at 100-120 compressions per minute",
                    "Continue until emergency help arrives",
                ]
            },
            {
                "title": "Recovery Position",
                "steps": [
                    "Kneel beside the person",
                    "Straighten both legs",
                    "Place one arm across chest",
                    "Bend near leg at the knee",
                    "Roll person toward you using the bent leg",
                    "Tilt head back to keep airway open",
                    "Monitor breathing and pulse",
                ]
            },
            {
                "title": "Treating Minor Wounds",
                "steps": [
                    "Wash hands with soap and water",
                    "Stop bleeding by applying gentle pressure",
                    "Clean wound with soap and clean water",
                    "Pat dry with clean cloth",
                    "Apply antibiotic ointment",
                    "Cover with sterile bandage if needed",
                    "Change bandage daily",
                ]
            },
        ]

        self.quizzes = [
            {
                "title": "First Aid Basics Quiz",
                "questions": [
                    {
                        "question": "What should you do first in case of severe bleeding?",
                        "options": [
                            "Apply direct pressure with a clean cloth",
                            "Wait for it to stop naturally",
                            "Pour water on it",
                            "Apply a tourniquet immediately"
                        ],
                        "correct": 0
                    },
                    {
                        "question": "What is the correct CPR compression rate?",
                        "options": [
                            "50-75 per minute",
                            "100-120 per minute",
                            "150-180 per minute",
                            "30-50 per minute"
                        ],
                        "correct": 1
                    },
                    {
                        "question": "For how long should you apply heat to a sprain?",
                        "options": [
                            "Immediately, for 20 minutes",
                            "After 48 hours, for 15-20 minutes",
                            "Never use heat",
                            "For 1 hour continuously"
                        ],
                        "correct": 1
                    },
                ]
            },
            {
                "title": "Health Knowledge Quiz",
                "questions": [
                    {
                        "question": "How many hours of sleep do adults need per night?",
                        "options": [
                            "4-5 hours",
                            "7-9 hours",
                            "10-12 hours",
                            "5-6 hours"
                        ],
                        "correct": 1
                    },
                ]
            }
        ]

    def show_articles(self):
        """Display articles"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Health Articles",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 15))

        for article in self.articles:
            self.create_article_card(article)

    def create_article_card(self, article):
        """Create article card"""
        card = create_card(self.content_frame)
        card.pack(fill="x", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Title
        title = ctk.CTkLabel(
            frame,
            text=article["title"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 8))

        # Category badge
        badge = ctk.CTkLabel(
            frame,
            text=f"  {article['category']}  ",
            font=ctk.CTkFont(size=9, family="Segoe UI", weight="bold"),
            text_color="#ffffff",
            fg_color=self.colors["info"],
            corner_radius=4,
            padx=8,
            pady=2
        )
        badge.pack(anchor="w", pady=(0, 8))

        # Excerpt
        excerpt = ctk.CTkLabel(
            frame,
            text=article["excerpt"],
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"],
            justify="left",
            wraplength=500
        )
        excerpt.pack(anchor="w", pady=(0, 10))

        # Read more button
        read_btn = ctk.CTkButton(
            frame,
            text="Read More",
            command=lambda a=article: self.show_article_full(a),
            fg_color=self.colors["accent"],
            hover_color=self.colors["danger"],
            font=ctk.CTkFont(size=10, family="Segoe UI", weight="bold"),
            height=28,
            width=100,
            corner_radius=6
        )
        read_btn.pack(anchor="w")

    def show_article_full(self, article):
        """Show full article"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Back button
        back_btn = ctk.CTkButton(
            self.content_frame,
            text="← Back",
            command=self.show_articles,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_secondary"],
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            height=28,
            width=80,
            corner_radius=6
        )
        back_btn.pack(anchor="w", pady=(0, 15))

        # Article content
        title = ctk.CTkLabel(
            self.content_frame,
            text=article["title"],
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 10))

        content = ctk.CTkLabel(
            self.content_frame,
            text=article["content"],
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=600
        )
        content.pack(anchor="w", pady=10)

    def show_tutorials(self):
        """Display tutorials"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="First Aid Tutorials",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 15))

        for tutorial in self.tutorials:
            self.create_tutorial_card(tutorial)

    def create_tutorial_card(self, tutorial):
        """Create tutorial card"""
        card = create_card(self.content_frame)
        card.pack(fill="x", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Title
        title = ctk.CTkLabel(
            frame,
            text=tutorial["title"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 12))

        # Steps
        for i, step in enumerate(tutorial["steps"], 1):
            step_label = ctk.CTkLabel(
                frame,
                text=f"{i}. {step}",
                font=ctk.CTkFont(size=11, family="Segoe UI"),
                text_color=self.colors["text_primary"],
                justify="left",
                wraplength=500
            )
            step_label.pack(anchor="w", pady=5)

    def show_quiz(self):
        """Display quiz selection"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Test Your Knowledge",
            font=ctk.CTkFont(size=20, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 15))

        for quiz in self.quizzes:
            self.create_quiz_card(quiz)

    def create_quiz_card(self, quiz):
        """Create quiz card"""
        card = create_card(self.content_frame)
        card.pack(fill="x", pady=10)

        frame = ctk.CTkFrame(card, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Title
        title = ctk.CTkLabel(
            frame,
            text=quiz["title"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        title.pack(anchor="w", pady=(0, 8))

        # Questions count
        questions_label = ctk.CTkLabel(
            frame,
            text=f"{len(quiz['questions'])} questions",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        questions_label.pack(anchor="w", pady=(0, 10))

        # Start button
        start_btn = ctk.CTkButton(
            frame,
            text="Start Quiz",
            command=lambda q=quiz: self.start_quiz(q),
            fg_color=self.colors["success"],
            hover_color="#059669",
            font=ctk.CTkFont(size=11, family="Segoe UI", weight="bold"),
            height=32,
            width=100,
            corner_radius=6
        )
        start_btn.pack(anchor="w")

    def start_quiz(self, quiz):
        """Start a quiz"""
        self.current_quiz = quiz
        self.quiz_score = 0
        self.quiz_progress = 0
        self.show_quiz_question()

    def show_quiz_question(self):
        """Show current quiz question"""
        if not self.current_quiz or self.quiz_progress >= len(self.current_quiz["questions"]):
            self.show_quiz_results()
            return

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        question_data = self.current_quiz["questions"][self.quiz_progress]

        # Progress
        progress_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Question {self.quiz_progress + 1} of {len(self.current_quiz['questions'])}",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        progress_label.pack(anchor="w", pady=(0, 5))

        progress_bar = ctk.CTkProgressBar(
            self.content_frame,
            value=(self.quiz_progress + 1) / len(self.current_quiz["questions"]),
            height=6,
            fg_color=self.colors["bg_tertiary"],
            progress_color=self.colors["success"]
        )
        progress_bar.pack(fill="x", pady=(0, 20))

        # Question
        question_label = ctk.CTkLabel(
            self.content_frame,
            text=question_data["question"],
            font=ctk.CTkFont(size=14, family="Segoe UI", weight="bold"),
            text_color=self.colors["text_primary"],
            justify="left",
            wraplength=500
        )
        question_label.pack(anchor="w", pady=(0, 20))

        # Options
        for i, option in enumerate(question_data["options"]):
            self.create_quiz_option(i, option, question_data["correct"])

    def create_quiz_option(self, index, option, correct_index):
        """Create quiz option button"""
        def check_answer():
            if index == correct_index:
                self.quiz_score += 1
            self.quiz_progress += 1
            self.show_quiz_question()

        btn = ctk.CTkButton(
            self.content_frame,
            text=option,
            command=check_answer,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["bg_secondary"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            height=40,
            corner_radius=8,
            justify="left"
        )
        btn.pack(fill="x", pady=8)

    def show_quiz_results(self):
        """Show quiz results"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        score_percentage = (self.quiz_score / len(self.current_quiz["questions"])) * 100 if self.current_quiz["questions"] else 0

        # Score display
        score_label = ctk.CTkLabel(
            self.content_frame,
            text="Quiz Completed!",
            font=ctk.CTkFont(size=24, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        score_label.pack(pady=20)

        score_card = create_card(self.content_frame)
        score_card.pack(fill="x", pady=20)

        score_value = ctk.CTkLabel(
            score_card,
            text=f"{self.quiz_score}/{len(self.current_quiz['questions'])}",
            font=ctk.CTkFont(size=48, family="Segoe UI", weight="bold"),
            text_color=self.colors["accent"]
        )
        score_value.pack(pady=20)

        percentage_label = ctk.CTkLabel(
            score_card,
            text=f"{int(score_percentage)}%",
            font=ctk.CTkFont(size=20, family="Segoe UI"),
            text_color=self.colors["text_secondary"]
        )
        percentage_label.pack(pady=(0, 20))

        # Back button
        back_btn = ctk.CTkButton(
            self.content_frame,
            text="Back to Quiz Selection",
            command=self.show_quiz,
            fg_color=self.colors["accent"],
            hover_color=self.colors["danger"],
            font=ctk.CTkFont(size=12, family="Segoe UI", weight="bold"),
            height=40,
            corner_radius=8
        )
        back_btn.pack(fill="x", pady=20)
