"""
Database Manager for Quick Aid Application
Uses SQLite for offline data storage
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime


class DatabaseManager:
    """Manages SQLite database operations"""

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "database" / "quickaid.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.connect()

    def connect(self):
        """Create database connection"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        """Execute a query"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return None

    def fetchone(self, query, params=None):
        """Fetch one row"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return None

    def fetchall(self, query, params=None):
        """Fetch all rows"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return []

    def initialize_database(self):
        """Create all necessary tables"""

        # Users table
        self.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                age INTEGER,
                gender TEXT,
                blood_group TEXT,
                allergies TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Emergency contacts table
        self.execute('''
            CREATE TABLE IF NOT EXISTS emergency_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                category TEXT NOT NULL,
                relationship TEXT,
                address TEXT,
                is_primary INTEGER DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # First aid kit items table
        self.execute('''
            CREATE TABLE IF NOT EXISTS first_aid_kit_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 1,
                min_quantity INTEGER DEFAULT 1,
                expiry_date TEXT,
                location TEXT,
                notes TEXT,
                in_stock INTEGER DEFAULT 1,
                last_checked TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Medicine library table
        self.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                generic_name TEXT,
                category TEXT,
                uses TEXT,
                dosage TEXT,
                adult_dosage TEXT,
                child_dosage TEXT,
                side_effects TEXT,
                warnings TEXT,
                storage TEXT,
                contraindications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Quiz scores table
        self.execute('''
            CREATE TABLE IF NOT EXISTS quiz_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                score INTEGER,
                total_questions INTEGER,
                percentage REAL,
                time_taken TEXT,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Learning progress table
        self.execute('''
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                score INTEGER,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Body parts data table
        self.execute('''
            CREATE TABLE IF NOT EXISTS body_parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_name TEXT NOT NULL UNIQUE,
                location TEXT,
                common_injuries TEXT,
                causes TEXT,
                symptoms TEXT,
                first_aid TEXT,
                dos TEXT,
                donts TEXT,
                recovery_tips TEXT,
                warning_signs TEXT,
                medicines TEXT,
                doctor_advice TEXT,
                prevention TEXT
            )
        ''')

        # First aid guides table
        self.execute('''
            CREATE TABLE IF NOT EXISTS first_aid_guides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                condition_name TEXT NOT NULL UNIQUE,
                category TEXT,
                definition TEXT,
                symptoms TEXT,
                immediate_action TEXT,
                step_by_step TEXT,
                dos TEXT,
                donts TEXT,
                recovery TEXT,
                warning_signs TEXT,
                doctor_recommendation TEXT,
                severity TEXT
            )
        ''')

        # Symptoms table
        self.execute('''
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT,
                description TEXT,
                related_conditions TEXT
            )
        ''')

        # Medical dictionary table
        self.execute('''
            CREATE TABLE IF NOT EXISTS medical_dictionary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL UNIQUE,
                definition TEXT,
                explanation TEXT,
                related_terms TEXT,
                category TEXT
            )
        ''')

        # Health tools history
        self.execute('''
            CREATE TABLE IF NOT EXISTS health_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_type TEXT NOT NULL,
                input_data TEXT,
                result TEXT,
                date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Special care guides
        self.execute('''
            CREATE TABLE IF NOT EXISTS special_care_guides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                content TEXT,
                emergency_info TEXT,
                precautions TEXT
            )
        ''')

        # Insert default data
        self.insert_default_data()

    def insert_default_data(self):
        """Insert default medical data into database"""

        # Check if data already exists
        if self.fetchone("SELECT COUNT(*) as count FROM body_parts")["count"] > 0:
            return

        # Body parts data
        body_parts_data = [
            ("Head", "Upper body", json.dumps(["Concussion", "Head injury", "Scalp wounds", "Headache"]),
             json.dumps(["Falls", "Sports injuries", "Accidents", "Physical assault"]),
             json.dumps(["Pain", "Dizziness", "Nausea", "Confusion", "Bleeding"]),
             json.dumps(["Keep person still", "Apply ice pack", "Monitor consciousness", "Call emergency if severe"]),
             json.dumps(["Keep head elevated", "Monitor symptoms", "Rest quietly"]),
             json.dumps(["Move the person unnecessarily", "Apply pressure if skull fracture suspected"]),
             json.dumps(["Rest in quiet room", "Gradual return to activity", "Follow doctor's advice"]),
             json.dumps(["Loss of consciousness", "Severe headache", "Vomiting", "Unequal pupils"]),
             json.dumps(["Pain relievers", "Ice packs", "Bandages"]),
             json.dumps(["See doctor if symptoms persist more than 24 hours"]),
             json.dumps(["Wear helmets", "Prevent falls", "Safe sports practices"])),

            ("Eyes", "Face", json.dumps(["Black eye", "Foreign object", "Chemical burn", "Scratched cornea"]),
             json.dumps(["Blows to face", "Debris", "Chemicals", "Rubbing eyes"]),
             json.dumps(["Pain", "Redness", "Tearing", "Blurred vision", "Swelling"]),
             json.dumps(["Flush with water if chemical", "Cover lightly if foreign object", "Do not rub", "Seek medical help"]),
             json.dumps(["Flush with clean water", "Cover with clean cloth", "Keep eye closed"]),
             json.dumps(["Rub the eye", "Remove embedded objects", "Apply pressure"]),
             json.dumps(["Use protective eyewear", "Rest eyes", "Follow-up with ophthalmologist"]),
             json.dumps(["Severe pain", "Vision loss", "Chemical exposure", "Object embedded"]),
             json.dumps(["Eye wash solution", "Sterile eye pads"]),
             json.dumps(["Seek immediate help for chemical burns or vision changes"]),
             json.dumps(["Wear safety glasses", "Avoid eye rubbing", "Regular eye checkups"])),

            ("Chest", "Torso", json.dumps(["Rib fracture", "Chest contusion", "Pneumothorax", "Heart attack"]),
             json.dumps(["Blunt trauma", "Falls", "Vehicle accidents", "Medical conditions"]),
             json.dumps(["Pain on breathing", "Bruising", "Shortness of breath", "Coughing blood"]),
             json.dumps(["Sit upright slightly", "Support injured area", "Monitor breathing", "Call emergency if severe"]),
             json.dumps(["Keep person calm", "Support with pillow", "Monitor vital signs"]),
             json.dumps(["Lie flat", "Apply heat", "Ignore breathing difficulty"]),
             json.dumps(["Gradual activity", "Deep breathing exercises", "Pain management"]),
             json.dumps(["Severe shortness of breath", "Blue lips", "Coughing blood", "Unequal chest movement"]),
             json.dumps(["Pain relievers (mild)", "Ice pack for bruising"]),
             json.dumps(["Emergency for breathing difficulty or cardiac symptoms"]),
             json.dumps(["Seat belt use", "Safe lifting", "Heart health awareness"])),

            ("Arms", "Upper limbs", json.dumps(["Fracture", "Sprain", "Dislocation", "Cuts"]),
             json.dumps(["Falls", "Sports", "Lifting injuries", "Accidents"]),
             json.dumps(["Pain", "Swelling", "Bruising", "Deformity", "Limited movement"]),
             json.dumps(["Immobilize with splint", "Apply ice", "Elevate", "Seek medical help"]),
             json.dumps(["Apply ice 20 minutes", "Immobilize", "Elevate above heart"]),
             json.dumps(["Move if deformity", "Apply heat initially", "Ignore numbness"]),
             json.dumps(["Rest", "Physical therapy", "Gradual movement"]),
             json.dumps(["Numbness", "Severe deformity", "Open wound", "No pulse"]),
             json.dumps(["Splints", "Bandages", "Ice packs", "Sling"]),
             json.dumps(["Get X-ray for suspected fracture"]),
             json.dumps(["Warm up before exercise", "Use proper form", "Wear protective gear"])),

            ("Legs", "Lower limbs", json.dumps(["Fracture", "Sprain", "DVT", "Cuts"]),
             json.dumps(["Falls", "Sports", "Accidents", "Prolonged sitting"]),
             json.dumps(["Pain", "Swelling", "Bruising", "Inability to bear weight"]),
             json.dumps(["Do not bear weight", "Immobilize", "Apply ice", "Elevate", "Seek medical help"]),
             json.dumps(["Rest", "Ice", "Compression", "Elevation (RICE)"]),
             json.dumps(["Walk on injured leg", "Apply heat", "Massage swelling"]),
             json.dumps(["Gradual weight bearing", "Physical therapy", "Supportive footwear"]),
             json.dumps(["Calf pain with swelling", "Shortness of breath", "Severe deformity"]),
             json.dumps(["Splints", "Crutches", "Ace bandages"]),
             json.dumps(["Emergency for DVT symptoms or open fracture"]),
             json.dumps(["Exercise regularly", "Stay hydrated", "Avoid prolonged sitting"])),

            ("Hands", "Upper limbs", json.dumps(["Fracture", "Burns", "Cuts", "Crush injury"]),
             json.dumps(["Falls", "Hot objects", "Sharp objects", "Machinery"]),
             json.dumps(["Pain", "Swelling", "Bleeding", "Deformity", "Loss of function"]),
             json.dumps(["Clean wound", "Apply pressure for bleeding", "Immobilize fracture", "Cool burns"]),
             json.dumps(["Clean with water", "Apply antibiotic", "Cover with bandage"]),
             json.dumps(["Ignore numbness", "Use dirty bandages", "Apply ice directly to burn"]),
             json.dumps(["Keep wound dry", "Change bandages", "Finger exercises"]),
             json.dumps(["Deep wound", "Tendon/nerve injury", "Severe burn", "Crush injury"]),
             json.dumps(["Bandages", "Antiseptic", "Burn gel", "Splints"]),
             json.dumps(["See hand specialist for complex injuries"]),
             json.dumps(["Use gloves", "Be cautious with tools", "Avoid hot surfaces"])),

            ("Feet", "Lower limbs", json.dumps(["Ankle sprain", "Fracture", "Blisters", "Cuts"]),
             json.dumps(["Twisting", "Falls", "Ill-fitting shoes", "Sports"]),
             json.dumps(["Pain", "Swelling", "Bruising", "Inability to walk"]),
             json.dumps(["Rest", "Ice", "Compression", "Elevation", "Avoid weight bearing"]),
             json.dumps(["RICE protocol", "Support with bandage", "Wear supportive shoe"]),
             json.dumps(["Walk on injury", "Apply heat", "Pop blisters"]),
             json.dumps(["Gradual activity", "Proper footwear", "Ankle strengthening"]),
             json.dumps(["Inability to move foot", "Severe swelling", "Deformity"]),
             json.dumps(["Elastic bandage", "Ice pack", "Bandages"]),
             json.dumps(["X-ray for suspected fracture"]),
             json.dumps(["Proper footwear", "Warm up", "Watch your step"])),

            ("Back", "Torso", json.dumps(["Strain", "Herniated disc", "Spinal injury", "Muscle spasm"]),
             json.dumps(["Lifting", "Poor posture", "Falls", "Accidents"]),
             json.dumps(["Pain", "Stiffness", "Numbness in legs", "Weakness"]),
             json.dumps(["Do not move if spinal injury suspected", "Apply cold then heat", "Seek medical help"]),
             json.dumps(["Lie comfortably", "Cold compress for 48 hours", "Then heat"]),
             json.dumps(["Move suspected spinal injury", "Ignore numbness", "Apply heat initially"]),
             json.dumps(["Core strengthening", "Proper posture", "Gradual return to activity"]),
             json.dumps(["Loss of bowel/bladder control", "Numbness in legs", "Weakness"]),
             json.dumps(["Hot/cold packs", "Pain relievers"]),
             json.dumps(["Emergency for spinal injury symptoms"]),
             json.dumps(["Lift with knees", "Exercise regularly", "Good posture"])),

            ("Neck", "Upper body", json.dumps(["Whiplash", "Strain", "Spinal injury", "Stiffness"]),
             json.dumps(["Vehicle accidents", "Poor posture", "Sports", "Falls"]),
             json.dumps(["Pain", "Stiffness", "Headache", "Limited movement", "Numbness"]),
             json.dumps(["Immobilize", "Do not move if spinal injury suspected", "Apply cold", "Seek medical help"]),
             json.dumps(["Keep neck still", "Cold compress", "Support with collar"]),
             json.dumps(["Move head if injury suspected", "Apply heat", "Massage"]),
             json.dumps(["Gradual movement", "Physical therapy", "Ergonomic adjustments"]),
             json.dumps(["Numbness in arms", "Difficulty breathing", "Severe pain"]),
             json.dumps(["Neck collar", "Cold pack", "Pain relievers"]),
             json.dumps(["Emergency for neurological symptoms"]),
             json.dumps(["Proper pillow", "Ergonomic workspace", "Exercise stretching"])),

            ("Abdomen", "Torso", json.dumps(["Contusion", "Appendicitis", "Internal bleeding", "Organ injury"]),
             json.dumps(["Blunt trauma", "Medical conditions", "Accidents"]),
             json.dumps(["Pain", "Swelling", "Nausea", "Vomiting", "Rigid abdomen"]),
             json.dumps(["Do not give food/water", "Position comfortably", "Seek emergency help"]),
             json.dumps(["Keep person still", "Monitor vital signs"]),
             json.dumps(["Give food/water", "Apply heat", "Take pain killers", "Ignore rigid abdomen"]),
             json.dumps(["Follow doctor's advice", "Gradual diet return", "Rest"]),
             json.dumps(["Rigid abdomen", "Severe pain", "Vomiting blood", "Fainting"]),
             json.dumps(["None for emergency situations"]),
             json.dumps(["Emergency for severe abdominal injury or appendicitis"]),
             json.dumps(["Wear seat belt", "Safe sports practices", "Healthy diet"]))
        ]

        for data in body_parts_data:
            self.execute('''
                INSERT OR IGNORE INTO body_parts
                (part_name, location, common_injuries, causes, symptoms, first_aid,
                 dos, donts, recovery_tips, warning_signs, medicines, doctor_advice, prevention)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

        # First aid guides data
        first_aid_data = [
            ("Burns", "Thermal", "Damage to skin from heat, chemicals, electricity, or radiation",
             json.dumps(["Redness", "Pain", "Blisters", "Swelling", "Charring"]),
             "Remove from heat source, cool with water",
             json.dumps(["Remove from heat source", "Cool with running water 10-20 min", "Remove jewelry/tight items",
                        "Cover with clean non-stick dressing", "Do not apply ice, butter, or ointments",
                        "Seek medical help for severe burns"]),
             json.dumps(["Cool with water", "Cover loosely", "Keep clean", "Elevate"]),
             json.dumps(["Apply ice directly", "Break blisters", "Apply butter/oil", "Use adhesive bandages"]),
             json.dumps(["Keep wound clean", "Change dressing daily", "Watch for infection"]),
             json.dumps(["Large area burned", "Face/hands/genitals burned", "Charring", "Electrical burn"]),
             "Seek medical help for 2nd/3rd degree burns",
             "High"),

            ("Cuts and Wounds", "Trauma", "Breaks in the skin surface",
             json.dumps(["Bleeding", "Pain", "Gaping wound", "Foreign objects"]),
             "Apply direct pressure with clean cloth",
             json.dumps(["Apply direct pressure", "Elevate wound above heart", "Clean with water",
                        "Apply antibiotic ointment", "Cover with bandage", "Seek help if bleeding doesn't stop"]),
             json.dumps(["Apply pressure", "Keep clean", "Elevate", "Watch for infection"]),
             json.dumps(["Remove large embedded objects", "Apply tourniquet unless trained", "Use dirty materials"]),
             json.dumps(["Keep dry 24 hours", "Change dressing daily", "Watch for infection signs"]),
             json.dumps(["Deep wound", "Bleeding won't stop", "Gaping wound", "Signs of infection"]),
             "Get stitches for deep wounds or seek help if infection develops",
             "Medium"),

            ("Fractures", "Trauma", "Break in a bone",
             json.dumps(["Pain", "Swelling", "Deformity", "Inability to move", "Bruising"]),
             "Immobilize the area, do not move injured person unnecessarily",
             json.dumps(["Do not move person", "Immobilize with splint", "Apply ice wrapped in cloth",
                        "Elevate if possible", "Call emergency or go to hospital"]),
             json.dumps(["Immobilize", "Apply ice", "Elevate", "Monitor circulation"]),
             json.dumps(["Move unnecessarily", "Try to realign bone", "Apply direct heat"]),
             json.dumps(["Follow doctor's treatment", "Physical therapy", "Gradual return to activity"]),
             json.dumps(["Open fracture", "Numbness", "No pulse below injury", "Severe deformity"]),
             "Seek immediate medical attention for X-ray and treatment",
             "High"),

            ("Choking", "Emergency", "Blockage of airway by foreign object",
             json.dumps(["Cannot breathe/talk", "Clutching throat", "Blue lips/face", "Unconsciousness"]),
             "Encourage coughing if can breathe, otherwise perform Heimlich maneuver",
             json.dumps(["Encourage coughing if can breathe", "Give 5 back blows", "Give 5 abdominal thrusts (Heimlich)",
                        "Alternate until object expelled", "Begin CPR if unconscious"]),
             json.dumps(["Stay calm", "Act quickly", "Call emergency", "Begin CPR if needed"]),
             json.dumps(["Slap back while standing upright", "Give water", "Perform Heimlich on infants same as adults"]),
             json.dumps(["Learn proper technique", "Prevent future episodes"]),
             json.dumps(["Unconsciousness", "Cannot breathe at all", "Turning blue"]),
             "Call emergency if obstruction not cleared within minutes",
             "Critical"),

            ("Heart Attack", "Cardiac", "Blockage of blood flow to heart muscle",
             json.dumps(["Chest pain/pressure", "Pain radiating to arm/jaw", "Shortness of breath",
                        "Nausea", "Cold sweat", "Dizziness"]),
             "Call emergency immediately, help person sit comfortably",
             json.dumps(["Call emergency immediately", "Help person sit comfortably", "Loosen tight clothing",
                        "Give aspirin if not allergic", "Begin CPR if no pulse", "Use AED if available"]),
             json.dumps(["Call help immediately", "Stay calm", "Keep person comfortable", "Monitor vitals"]),
             json.dumps(["Leave person alone", "Drive yourself to hospital", "Ignore symptoms"]),
             json.dumps(["Follow cardiac rehabilitation", "Lifestyle changes", "Take prescribed medications"]),
             json.dumps(["Chest pain lasting more than minutes", "Difficulty breathing", "Unconsciousness"]),
             "Call emergency immediately - every minute counts",
             "Critical"),

            ("Snake Bite", "Wildlife", "Venomous injection from snake fangs",
             json.dumps(["Two puncture wounds", "Pain", "Swelling", "Nausea", "Difficulty breathing"]),
             "Keep person calm and still, immobilize bitten area",
             json.dumps(["Keep person calm and still", "Remove jewelry before swelling", "Immobilize bitten area below heart level",
                        "Clean wound", "Do not cut/suck/tourniquet", "Call emergency immediately"]),
             json.dumps(["Keep calm", "Immobilize", "Remove jewelry", "Seek immediate help", "Note snake description"]),
             json.dumps(["Cut wound", "Suck out venom", "Apply tourniquet", "Apply ice", "Give alcohol"]),
             json.dumps(["Hospital observation", "Antivenom treatment if needed", "Monitor for complications"]),
             json.dumps(["Difficulty breathing", "Severe swelling", "Bleeding", "Muscle weakness"]),
             "Seek immediate emergency care - antivenom may be needed",
             "Critical"),

            ("Electric Shock", "Electrical", "Injury from electrical current passing through body",
             json.dumps(["Burns at contact points", "Unconsciousness", "Cardiac arrest", "Muscle spasms"]),
             "Do NOT touch person if still in contact with electricity",
             json.dumps(["Do not touch person directly", "Turn off power source", "Separate using non-conductive object",
                        "Call emergency", "Begin CPR if no pulse/breathing"]),
             json.dumps(["Ensure power is off", "Use dry non-conductive object", "Begin CPR if needed", "Call emergency"]),
             json.dumps(["Touch person directly if current still on", "Use wet objects to separate"]),
             json.dumps(["Cardiac monitoring", "Treatment for burns", "Neurological assessment"]),
             json.dumps(["Unconsciousness", "Cardiac arrest", "Severe burns", "Trouble breathing"]),
             "Seek emergency care - internal injuries possible even with minor external signs",
             "Critical"),

            ("Drowning", "Water", "Respiratory impairment from submersion in liquid",
             json.dumps(["Not breathing", "Coughing", "Vomiting water", "Unconsciousness"]),
             "Remove from water, check breathing, begin CPR if needed",
             json.dumps(["Call for help", "Reach/throw - don't enter unless trained", "Remove from water if safe",
                        "Check breathing and pulse", "Begin CPR if needed", "Place in recovery position if breathing"]),
             json.dumps(["Call for help", "Begin CPR immediately if not breathing", "Keep person warm"]),
             json.dumps(["Enter water untrained", "Give up on CPR too early", "Give Heimlich for water removal"]),
             json.dumps(["Hospital observation for near-drowning", "Watch for secondary drowning"]),
             json.dumps(["Not breathing after rescue", "Unconscious", "Vomiting"]),
             "Seek emergency care even if person appears fine after rescue",
             "Critical"),

            ("Heat Stroke", "Environmental", "Life-threatening heat illness with core temp >40C",
             json.dumps(["High body temperature", "Hot dry skin", "Confusion", "Unconsciousness", "Rapid pulse"]),
             "Move to cool area, cool body rapidly, call emergency",
             json.dumps(["Move to cool/shaded area", "Remove excess clothing", "Cool with water/ice packs to neck/armpits/groin",
                        "Fan if possible", "Call emergency", "Monitor temperature"]),
             json.dumps(["Cool rapidly", "Monitor vital signs", "Call for help", "Keep in cool area"]),
             json.dumps(["Use ice water bath", "Give fluids if unconscious", "Delay cooling"]),
             json.dumps(["Gradual heat acclimatization", "Monitor for heat intolerance"]),
             json.dumps(["Confusion", "Unconsciousness", "Temperature >40C", "Seizures"]),
             "This is a medical emergency - call for help immediately",
             "Critical"),

            ("Asthma Attack", "Respiratory", "Narrowing and swelling of airways",
             json.dumps(["Wheezing", "Shortness of breath", "Chest tightness", "Coughing", "Anxiety"]),
             "Help person sit up, use rescue inhaler, stay calm",
             json.dumps(["Help person sit upright", "Help use rescue inhaler", "Stay calm and reassure",
                        "Loosen tight clothing", "Call emergency if no improvement after 15 min"]),
             json.dumps(["Stay calm", "Use inhaler as prescribed", "Sit upright", "Take slow breaths"]),
             json.dumps(["Lie flat", "Go outside into cold air", "Ignore worsening symptoms"]),
             json.dumps(["Follow asthma action plan", "Avoid triggers", "Take controller medication"]),
             json.dumps(["Blue lips/face", "Cannot speak", "Confusion", "Exhaustion"]),
             "Call emergency if rescue inhaler not working or severe attack",
             "High"),

            ("Seizures", "Neurological", "Abnormal electrical activity in brain",
             json.dumps(["Uncontrolled movements", "Loss of consciousness", "Confusion after", "Biting tongue"]),
             "Protect from injury, do not restrain, time the seizure",
             json.dumps(["Protect head", "Move dangerous objects away", "Do not restrain", "Time the seizure",
                        "Place in recovery position after", "Stay calm and stay with person"]),
             json.dumps(["Protect from injury", "Time the seizure", "Stay calm", "Place on side after seizure"]),
             json.dumps(["Hold person down", "Put anything in mouth", "Give water/food during seizure"]),
             json.dumps(["Follow doctor's treatment plan", "Take medication as prescribed", "Avoid triggers"]),
             json.dumps(["Seizure lasts >5 min", "Multiple seizures", "Injury during seizure", "No known seizure history"]),
             "Call emergency for first seizure or seizure lasting >5 minutes",
             "High"),

            ("Allergic Reaction", "Immune", "Hypersensitive immune response",
             json.dumps(["Hives", "Swelling", "Itching", "Difficulty breathing", "Nausea"]),
             "Remove allergen, give antihistamine, use EpiPen if severe",
             json.dumps(["Remove allergen if known", "Give antihistamine", "Use EpiPen if available and prescribed for anaphylaxis",
                        "Call emergency if severe", "Monitor breathing"]),
             json.dumps(["Remove allergen", "Stay calm", "Monitor breathing", "Call emergency if severe"]),
             json.dumps(["Ignore symptoms", "Wait to see if improves if severe"]),
             json.dumps(["Identify and avoid allergens", "Carry EpiPen if prescribed", "Inform others of allergies"]),
             json.dumps(["Swelling of face/throat", "Difficulty breathing", "Dizziness", "Rapid pulse"]),
             "Call emergency immediately for signs of anaphylaxis",
             "High")
        ]

        for data in first_aid_data:
            self.execute('''
                INSERT OR IGNORE INTO first_aid_guides
                (condition_name, category, definition, symptoms, immediate_action, step_by_step,
                 dos, donts, recovery, warning_signs, doctor_recommendation, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

        # Symptoms data
        symptoms_data = [
            ("Fever", "General", "Elevated body temperature above normal", json.dumps(["Flu", "Infection", "Malaria", "COVID-19"])),
            ("Headache", "Neurological", "Pain in head or upper neck", json.dumps(["Migraine", "Tension", "Sinusitis", "Dehydration"])),
            ("Cough", "Respiratory", "Sudden expulsion of air from lungs", json.dumps(["Cold", "Flu", "Bronchitis", "Pneumonia"])),
            ("Nausea", "Digestive", "Feeling of sickness with urge to vomit", json.dumps(["Food poisoning", "Pregnancy", "Migraine", "Viral illness"])),
            ("Chest Pain", "Cardiac", "Discomfort or pain in chest area", json.dumps(["Heart attack", "Angina", "Heartburn", "Muscle strain"])),
            ("Abdominal Pain", "Digestive", "Pain in stomach area", json.dumps(["Appendicitis", "Gastritis", "Food poisoning", "Gas"])),
            ("Dizziness", "Neurological", "Feeling lightheaded or unbalanced", json.dumps(["Dehydration", "Low blood sugar", "Anemia", "Inner ear problem"])),
            ("Shortness of Breath", "Respiratory", "Difficulty breathing", json.dumps(["Asthma", "Pneumonia", "Heart failure", "Anxiety"])),
            ("Vomiting", "Digestive", "Forceful expulsion of stomach contents", json.dumps(["Food poisoning", "Viral infection", "Migraine", "Pregnancy"])),
            ("Fatigue", "General", "Extreme tiredness not relieved by rest", json.dumps(["Anemia", "Depression", "Thyroid disorder", "Chronic fatigue"])),
            ("Joint Pain", "Musculoskeletal", "Discomfort in joints", json.dumps(["Arthritis", "Injury", "Gout", "Infection"])),
            ("Skin Rash", "Dermatological", "Change in skin appearance or texture", json.dumps(["Allergy", "Infection", "Eczema", "Medication reaction"])),
            ("Sore Throat", "Respiratory", "Pain or irritation in throat", json.dumps(["Strep throat", "Viral infection", "Tonsillitis", "Allergies"])),
            ("Back Pain", "Musculoskeletal", "Discomfort in back region", json.dumps(["Muscle strain", "Herniated disc", "Arthritis", "Kidney problem"])),
            ("Numbness", "Neurological", "Loss of sensation", json.dumps(["Nerve compression", "Diabetes", "Stroke", "Vitamin deficiency"]))
        ]

        for data in symptoms_data:
            self.execute('''
                INSERT OR IGNORE INTO symptoms (name, category, description, related_conditions)
                VALUES (?, ?, ?, ?)
            ''', data)

        # Medicine data
        medicine_data = [
            ("Paracetamol", "Acetaminophen", "Pain relief", "Pain reliever and fever reducer",
             "500-1000mg every 4-6 hours", "500-1000mg every 4-6 hours", "10-15mg/kg every 4-6 hours",
             json.dumps(["Nausea", "Allergic reaction (rare)", "Liver damage (overdose)"]),
             json.dumps(["Do not exceed 4000mg daily", "Avoid with alcohol", "Caution with liver disease"]),
             json.dumps(["Store at room temperature", "Keep away from moisture", "Keep out of reach of children"]),
             json.dumps(["Liver disease", "Alcohol dependency", "Allergy to paracetamol"])),

            ("ORS (Oral Rehydration Solution)", "Electrolyte solution", "Rehydration", "Treats dehydration from diarrhea, vomiting",
             "Drink as needed", "200-400ml after each loose stool", "100-200ml after each loose stool",
             json.dumps(["None significant"]),
             json.dumps(["Do not force if vomiting", "Seek help if cannot keep fluids down"]),
             json.dumps(["Store in cool dry place", "Use within 24 hours of mixing"]),
             json.dumps(["Severe vomiting requiring IV", "Intestinal blockage"])),

            ("Betadine Solution", "Povidone-iodine", "Antiseptic", "Prevents and treats wound infections",
             "Apply to wound area", "Apply to wound 1-2 times daily", "Apply to wound 1-2 times daily",
             json.dumps(["Skin irritation", "Allergic reaction (iodine sensitivity)"]),
             json.dumps(["Do not use on large wounds", "Avoid in thyroid disease", "Avoid in pregnancy (large amounts)"]),
             json.dumps(["Store at room temperature", "Keep container tightly closed"]),
             json.dumps(["Iodine allergy", "Thyroid disorders"])),
        ]

        for data in medicine_data:
            self.execute('''
                INSERT OR IGNORE INTO medicines
                (name, generic_name, category, uses, dosage, adult_dosage, child_dosage, side_effects, warnings, storage, contraindications)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

        # Medical dictionary entries
        dictionary_data = [
            ("Cardiopulmonary Resuscitation", "Emergency procedure to restore breathing and heartbeat",
             "CPR involves chest compressions and rescue breaths to maintain circulation when the heart stops beating.",
             json.dumps(["Heart attack", "Cardiac arrest", "First aid", "Emergency care"]), "Emergency"),
            ("Tourniquet", "Device to stop bleeding by compressing blood vessels",
             "A tourniquet is a tight band applied around a limb to stop severe bleeding in emergency situations.",
             json.dumps(["Bleeding control", "Emergency", "First aid"]), "Equipment"),
            ("Anaphylaxis", "Severe allergic reaction that can be life-threatening",
             "Anaphylaxis is a rapid, severe allergic reaction requiring immediate treatment with epinephrine.",
             json.dumps(["Allergy", "EpiPen", "Emergency", "Hypersensitivity"]), "Condition"),
            ("Concussion", "Mild traumatic brain injury from impact",
             "A concussion occurs when the brain is shaken inside the skull from a blow to the head.",
             json.dumps(["Head injury", "Trauma", "Brain injury", "Sports injury"]), "Condition"),
            ("Heimlich Maneuver", "First aid procedure for choking",
             "The Heimlich maneuver uses abdominal thrusts to dislodge objects blocking the airway.",
             json.dumps(["Choking", "Airway obstruction", "First aid", "Emergency"]), "Procedure"),
        ]

        for data in dictionary_data:
            self.execute('''
                INSERT OR IGNORE INTO medical_dictionary (term, definition, explanation, related_terms, category)
                VALUES (?, ?, ?, ?, ?)
            ''', data)

        # Special care guides
        special_care_data = [
            ("Children", "Choking Prevention", "Keep small objects away from children. Cut food into small pieces. Supervise eating.",
             json.dumps(["Small objects away", "Cut food small", "No running with food", "Supervise play"]),
             json.dumps(["Learn infant/child CPR", "Know emergency numbers", "First aid training for parents"])),
            ("Children", "Fever Management", "Use age-appropriate medication. Keep child comfortable. Monitor temperature.",
             json.dumps(["Use children's paracetamol", "Dress lightly", "Plenty of fluids", "Monitor for seizures"]),
             json.dumps(["Avoid aspirin (Reye's syndrome)", "Seek help if fever >103°F or lasting >3 days"])),
            ("Pregnant Women", "Morning Sickness", "Eat small frequent meals. Stay hydrated. Avoid triggers.",
             json.dumps(["Small meals", "Ginger tea", "Bland foods", "Morning snack before rising"]),
             json.dumps(["Seek help if unable to keep fluids down", "Unusual weight loss"])),
            ("Pregnant Women", "Leg Cramps", "Stretch before bed. Stay hydrated. Maintain electrolyte balance.",
             json.dumps(["Stretch calf muscles", "Magnesium supplements (consult doctor)", "Stay active"]),
             json.dumps(["Severe swelling", "One leg only swollen (possible DVT)"])),
            ("Senior Citizens", "Fall Prevention", "Remove tripping hazards. Use grab bars. Wear proper footwear.",
             json.dumps(["Clear walkways", "Good lighting", "Non-slip mats", "Handrails on stairs"]),
             json.dumps(["Regular exercise", "Vision checks", "Medication review for dizziness-causing drugs"])),
            ("Senior Citizens", "Medication Management", "Use pill organizers. Set alarms. Keep medication list.",
             json.dumps(["Pill organizer", "Medication list", "Regular pharmacy reviews", "One pharmacy"]),
             json.dumps(["Ask about drug interactions", "Report side effects", "Don't share medications"])),
        ]

        for data in special_care_data:
            self.execute('''
                INSERT OR IGNORE INTO special_care_guides (category, topic, content, emergency_info, precautions)
                VALUES (?, ?, ?, ?, ?)
            ''', data)

        # Default emergency contacts
        emergency_contacts = [
            ("Emergency Services (National)", "112", "Emergency", "National", "", 1, "Universal emergency number"),
            ("Ambulance", "108", "Emergency", "Ambulance", "", 1, "Medical emergency ambulance service"),
            ("Police", "100", "Emergency", "Police", "", 0, "Police emergency"),
            ("Fire Department", "101", "Emergency", "Fire", "", 0, "Fire emergency"),
            ("Women Helpline", "1091", "Emergency", "Women Safety", "", 0, "Women distress helpline"),
            ("Child Helpline", "1098", "Emergency", "Child Safety", "", 0, "Child in distress helpline"),
            ("Poison Control", "1066", "Emergency", "Poison", "", 0, "Poison information center"),
        ]

        for data in emergency_contacts:
            self.execute('''
                INSERT OR IGNORE INTO emergency_contacts (name, phone, category, relationship, address, is_primary, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data)


if __name__ == "__main__":
    db = DatabaseManager()
    db.initialize_database()
    print("Database initialized successfully!")
    db.close()
