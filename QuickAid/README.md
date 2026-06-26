# Quick Aid - Smart First Aid & Emergency Care System

<p align="center">
  <img src="assets/icons/icon.png" alt="QuickAid Logo" width="200"/>
</p>

<p align="center">
  <strong>A Complete Offline Healthcare & First Aid Desktop Application</strong>
</p>

<p align="center">
  B.Tech Community Service Project (CSP)
</p>

---

## Features

### 1. Interactive Human Body System
- Clickable body parts (Head, Eyes, Ears, Nose, Mouth, Neck, Shoulders, Chest, Back, Arms, Hands, Abdomen, Legs, Feet)
- Male and Female body options
- Front and Back view toggle
- Common injuries, causes, symptoms for each body part
- First aid treatment, do's and don'ts
- Recovery tips and warning signs
- When to see a doctor

### 2. Complete First Aid Guide
- **Critical Emergencies**: Heart Attack, Stroke, Choking, Drowning, Electric Shock
- **Trauma & Injuries**: Burns, Cuts, Fractures, Sprains, Head Injuries
- **Animal & Insect**: Snake Bite, Dog Bite, Insect Stings
- **Medical Emergencies**: Asthma, Seizures, Allergic Reactions
- **Environmental**: Heat Stroke, Hypothermia, Frostbite

### 3. Smart Symptom Checker
- Rule-based offline symptom analysis
- Select multiple symptoms from checkboxes
- Get possible conditions and recommendations
- Warning alerts for serious conditions
- Doctor consultation advice

### 4. Emergency Medicine Library
- Searchable medicine database
- Categories: Painkillers, Antibiotics, Antiseptics, First Aid items
- Detailed info: Dosage, Side effects, Warnings, Storage
- Age-appropriate dosage information

### 5. First Aid Kit Manager
- Track available/missing items
- Add custom items
- Set minimum quantity thresholds
- View completion percentage
- Expiry date notifications

### 6. Emergency Contacts
- Categories: Family, Doctors, Hospitals, Emergency Services
- Quick call buttons
- Add/Edit/Delete contacts
- Set primary contacts

### 7. SOS Emergency Screen
- Large SOS button for emergencies
- Emergency numbers:
  - National Emergency: 112
  - Ambulance: 108
  - Police: 100
  - Fire: 101
  - Women Helpline: 1091
  - Child Helpline: 1098
- Emergency instructions
- Quick emergency actions

### 8. Medical Learning Center
- Health awareness articles
- First aid tutorials
- Interactive quiz system
- Score tracking
- Achievement badges
- Progress tracking

### 9. Health Tools
- BMI Calculator
- Water Intake Calculator
- Daily Calorie Estimator
- Health risk assessment

### 10. Special Care Guides
- Children care guides
- Women's health
- Senior citizen care
- Pregnancy care
- Age-specific emergency guidance

### 11. Medical Dictionary
- 200+ medical terms
- Detailed definitions
- Related terms
- Alphabetical organization
- Search functionality

### 12. Voice Assistant
- Read treatment instructions aloud
- Text-to-speech using pyttsx3
- Adjustable speed and volume
- Hands-free emergency guidance

### 13. PDF Report Generator
- Symptom checker reports
- Quiz result certificates
- First aid kit inventory
- Health calculation records
- Contact list exports

---

## Technology Stack

- **Language**: Python 3.9+
- **GUI Framework**: CustomTkinter
- **Database**: SQLite
- **Image Processing**: Pillow
- **Text-to-Speech**: pyttsx3
- **PDF Generation**: ReportLab
- **Calculations**: NumPy

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Download the Project
```bash
git clone <repository-url>
cd QuickAid
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

---

## Project Structure

```
QuickAid/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── README.md               # Documentation
│
├── database/
│   ├── database.py         # Database manager
│   └── quickaid.db         # SQLite database (auto-created)
│
├── modules/
│   ├── body_system.py      # Interactive body map
│   ├── first_aid.py        # First aid guide
│   ├── symptom_checker.py  # Symptom analysis
│   ├── medicine_library.py # Medicine database
│   ├── first_aid_kit.py    # Kit manager
│   ├── contacts.py         # Emergency contacts
│   ├── emergency.py        # SOS screen
│   ├── learning_center.py  # Learning & quiz
│   ├── health_tools.py     # Health calculators
│   ├── dictionary.py       # Medical dictionary
│   ├── special_care.py     # Special care guides
│   ├── voice_assistant.py  # Text-to-speech
│   └── pdf_generator.py    # PDF reports
│
├── gui/
│   ├── dashboard.py        # Main dashboard
│   ├── sidebar.py          # Navigation sidebar
│   ├── themes.py           # Theme manager
│   └── settings.py         # Settings page
│
├── assets/
│   ├── images/             # Application images
│   └── icons/              # Application icons
│
├── reports/                # Generated PDF reports
└── data/                   # Application data
```

---

## How to Use

### Dashboard
- Quick action buttons for common tasks
- Statistics overview
- Emergency contacts widget
- First aid kit status

### Interactive Body Map
1. Select gender (Male/Female)
2. Choose view (Front/Back)
3. Click on any body part
4. View injuries, causes, symptoms
5. Follow first aid instructions

### Symptom Checker
1. Select symptoms from checkboxes
2. Click "Analyze Symptoms"
3. View possible conditions
4. Read recommendations
5. Check warning alerts

### First Aid Guide
1. Search or browse conditions
2. Click on condition name
3. Read step-by-step instructions
4. Follow do's and don'ts
5. Know when to seek help

### Medicine Library
1. Use search bar to find medicines
2. Or browse by category
3. View dosage, side effects
4. Check storage instructions
5. Read warnings

### First Aid Kit
1. Add new items with quantity
2. Check items as "in stock"
3. View completion percentage
4. Set expiry dates
5. Generate kit report

### SOS Emergency
1. Large SOS button for emergencies
2. Quick call buttons for:
   - National Emergency: 112
   - Ambulance: 108
   - Police: 100
   - Fire: 101
3. Follow emergency instructions

---

## Key Features for Different Users

### For Households
- Emergency reference for families
- First aid kit manager
- Child and senior care guides

### For Schools & Colleges
- Health education tool
- First aid training
- Anatomy learning

### For Communities
- Emergency preparedness
- Health awareness
- Medical terminology learning

### For Healthcare Professionals
- Quick reference guide
- Patient education tool
-- Symptom documentation

---

## Emergency Numbers (India)

| Service | Number |
|---------|--------|
| National Emergency | 112 |
| Ambulance | 108 |
| Police | 100 |
| Fire Department | 101 |
| Women Helpline | 1091 |
| Child Helpline | 1098 |
| Poison Control | 1066 |

---

## Disclaimer

This application is for educational and informational purposes only. It should not replace professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider for any medical condition.

In case of a medical emergency, call local emergency services immediately.

---

## License

This project is developed as a B.Tech Community Service Project (CSP) and is intended for educational purposes.

---

## Acknowledgments

- CustomTkinter for the modern UI components
- ReportLab for PDF generation
- pyttsx3 for text-to-speech capabilities
- Open source medical information resources

---

## Contact

For queries or feedback regarding this project:
- Project Team: B.Tech Community Service Project
- Year: 2024-2025

---

<p align="center">
  <strong>Made with care for community health and safety</strong>
</p>
