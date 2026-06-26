"""
Quick Aid - Smart First Aid & Emergency Care System
Unified Flask Application - Serves React Frontend + Python Backend API
"""

from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import os
import sys
import json
from pathlib import Path

# Add QuickAid to path for database
sys.path.insert(0, str(Path(__file__).parent / "QuickAid"))
from database.database import DatabaseManager

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# Initialize database
db = DatabaseManager()
db.initialize_database()

# Quiz Questions Data
quiz_questions = [
    {"id": 1, "category": "burns", "question": "What is the first thing you should do for a minor burn?", "options": ["Apply ice directly", "Run cool water over it", "Apply butter or oil", "Pop any blisters"], "correct": 1, "explanation": "Cool water helps reduce temperature and prevents further tissue damage."},
    {"id": 2, "category": "burns", "question": "How long should you cool a burn under running water?", "options": ["30 seconds", "2 minutes", "10-20 minutes", "1 hour"], "correct": 2, "explanation": "Cooling a burn for 10-20 minutes helps reduce pain and prevent further damage."},
    {"id": 3, "category": "choking", "question": "What is the first step when someone is choking but can still cough?", "options": ["Perform abdominal thrusts", "Encourage them to cough", "Give them water", "Slap their back hard"], "correct": 1, "explanation": "If the person can still cough, encourage coughing to clear the obstruction."},
    {"id": 4, "category": "choking", "question": "How many back blows should you give to a choking adult?", "options": ["1", "3", "5", "10"], "correct": 2, "explanation": "Give 5 back blows between the shoulder blades."},
    {"id": 5, "category": "bleeding", "question": "What is the correct way to control severe bleeding?", "options": ["Apply direct pressure with clean cloth", "Wash with water", "Apply a tourniquet immediately", "Let it bleed to clean wound"], "correct": 0, "explanation": "Direct pressure with a clean cloth is the most effective method."},
    {"id": 6, "category": "fractures", "question": "What should you do if you suspect a fracture?", "options": ["Try to straighten the bone", "Move the person immediately", "Immobilize the area and seek medical help", "Apply heat to reduce pain"], "correct": 2, "explanation": "Never try to straighten a fracture. Immobilize and seek medical attention."},
    {"id": 7, "category": "electric_shock", "question": "What is the first step in helping someone with an electric shock?", "options": ["Touch them to pull them away", "Turn off the power source", "Pour water on them", "Call emergency services first"], "correct": 1, "explanation": "Always turn off the power source first. Never touch the person directly."},
    {"id": 8, "category": "cpr", "question": "What is the correct ratio of chest compressions to breaths for adult CPR?", "options": ["15:2", "30:2", "10:1", "20:3"], "correct": 1, "explanation": "Perform 30 chest compressions followed by 2 rescue breaths."},
    {"id": 9, "category": "stroke", "question": "What does F.A.S.T. stand for in stroke recognition?", "options": ["Face, Arms, Speech, Time", "Fast, Alert, Strong, Tall", "Force, Action, Speed, Talk", "First Aid, Safety, Treatment"], "correct": 0, "explanation": "F.A.S.T. helps identify stroke: Face drooping, Arms weakness, Speech slurred, Time to call emergency."},
    {"id": 10, "category": "general", "question": "What should be included in a first aid kit?", "options": ["Prescription medications", "Antiseptic and bandages", "Sharp knives", "Alcoholic beverages"], "correct": 1, "explanation": "A basic first aid kit should include antiseptic, bandages, gauze, and gloves."},
]

# Body Map First Aid Data
body_parts = {
    "head": {"name": "Head", "conditions": ["Head Injury", "Concussion", "Headache"], "first_aid": ["Keep the person still", "Apply cold compress", "Monitor consciousness", "Call emergency if vomiting or confusion"]},
    "face": {"name": "Face", "conditions": ["Nosebleed", "Facial Injury", "Eye Injury"], "first_aid": ["Sit forward for nosebleed", "Pinch nose for 10 minutes", "Do not rub eyes", "Cover eye injuries gently"]},
    "neck": {"name": "Neck", "conditions": ["Neck Strain", "Whiplash", "Spinal Injury"], "first_aid": ["Do not move the person", "Immobilize neck", "Call emergency", "Keep person calm"]},
    "chest": {"name": "Chest", "conditions": ["Chest Pain", "Rib Injury", "Heart Attack"], "first_aid": ["Call emergency immediately", "Keep person sitting", "Loosen tight clothing", "Aspirin if not allergic"]},
    "abdomen": {"name": "Abdomen", "conditions": ["Abdominal Pain", "Appendicitis", "Stomach Injury"], "first_aid": ["Do not give food or water", "Apply cold compress", "Seek medical help", "Monitor vital signs"]},
    "arm-left": {"name": "Left Arm", "conditions": ["Fracture", "Sprain", "Cut/Wound"], "first_aid": ["Immobilize with splint", "Apply ice for swelling", "Elevate if possible", "Apply pressure for bleeding"]},
    "arm-right": {"name": "Right Arm", "conditions": ["Fracture", "Sprain", "Cut/Wound"], "first_aid": ["Immobilize with splint", "Apply ice for swelling", "Elevate if possible", "Apply pressure for bleeding"]},
    "hand": {"name": "Hands", "conditions": ["Burns", "Cuts", "Fractures"], "first_aid": ["Cool burns with water", "Apply pressure for cuts", "Immobilize fractures", "Keep elevated"]},
    "leg-left": {"name": "Left Leg", "conditions": ["Fracture", "Sprain", "Deep Vein Thrombosis"], "first_aid": ["Do not bear weight", "Immobilize with splint", "Apply ice", "Elevate if possible"]},
    "leg-right": {"name": "Right Leg", "conditions": ["Fracture", "Sprain", "Deep Vein Thrombosis"], "first_aid": ["Do not bear weight", "Immobilize with splint", "Apply ice", "Elevate if possible"]},
    "foot": {"name": "Feet", "conditions": ["Ankle Sprain", "Fracture", "Blisters"], "first_aid": ["RICE: Rest, Ice, Compression, Elevation", "Support with bandage", "Do not pop blisters"]},
    "back": {"name": "Back", "conditions": ["Back Pain", "Spinal Injury", "Muscle Strain"], "first_aid": ["Do not move if spinal injury suspected", "Apply cold then heat", "Rest in comfortable position", "Seek medical help"]},
}

# Emergency Workflows
emergency_workflows = {
    "bleeding": {"title": "Severe Bleeding", "steps": ["Apply direct pressure with clean cloth", "Elevate the wound above heart", "Apply additional bandages if needed", "Use tourniquet only as last resort", "Call emergency services"]},
    "burns": {"title": "Burns", "steps": ["Remove from heat source", "Cool with running water for 10-20 min", "Remove jewelry/tight items", "Cover with clean, non-fluffy dressing", "Do not apply ice, butter, or ointments", "Seek medical help for severe burns"]},
    "choking": {"title": "Choking", "steps": ["Encourage coughing if they can breathe", "Give 5 back blows between shoulder blades", "Give 5 abdominal thrusts (Heimlich)", "Alternate until obstruction cleared", "Call emergency if unconscious"]},
    "fracture": {"title": "Fracture", "steps": ["Do not move the injured area", "Immobilize with splint", "Apply ice to reduce swelling", "Elevate if possible", "Seek medical help immediately"]},
    "electric_shock": {"title": "Electric Shock", "steps": ["Do NOT touch the person directly", "Turn off power source", "Separate using dry non-conductive object", "Call emergency services", "Begin CPR if not breathing"]},
    "heart_attack": {"title": "Heart Attack", "steps": ["Call emergency immediately", "Help person sit in comfortable position", "Loosen tight clothing", "Give aspirin if not allergic", "Be ready to perform CPR"]},
    "stroke": {"title": "Stroke", "steps": ["Call emergency immediately", "Note time symptoms started", "Keep person lying down", "Do not give food or drink", "Reassure and keep calm"]},
    "drowning": {"title": "Drowning", "steps": ["Call for help", "Reach or throw - don't enter unless trained", "Remove from water if safe", "Check breathing and pulse", "Begin CPR if needed"]},
}

# Preparedness Guides
preparedness_guides = {
    "earthquake": {"title": "Earthquake Safety", "steps": ["Drop, Cover, Hold On", "Stay away from windows and heavy objects", "If outdoors, move away from buildings", "After shaking, evacuate carefully", "Check for injuries and gas leaks", "Be prepared for aftershocks"], "supplies": ["Water (1 gallon per day)", "Non-perishable food", "Flashlight and batteries", "First aid kit", "Whistle", "Dust masks"]},
    "fire": {"title": "Fire Safety", "steps": ["Get out, stay out, call for help", "Crawl low under smoke", "Feel doors before opening", "Use stairs, never elevators", "Meet at designated spot", "Do not go back inside"], "supplies": ["Smoke detectors", "Fire extinguisher", "Escape ladder", "Emergency blankets"]},
    "flood": {"title": "Flood Safety", "steps": ["Move to higher ground immediately", "Do not walk in moving water", "Do not drive through flooded roads", "Avoid contact with floodwater", "Stay informed via radio", "Return home only when safe"], "supplies": ["Waterproof containers", "Life jackets", "Rubber boots", "Bottled water", "Battery-powered radio"]},
    "cyclone": {"title": "Cyclone/Hurricane Safety", "steps": ["Board windows and secure doors", "Move to interior room", "Stay away from windows", "Do not go outside during eye", "Keep emergency kit nearby", "Wait for official all-clear"], "supplies": ["Plywood", "Emergency radio", "Canned food", "Water supply", "Batteries"]},
}

# ============ Serve React Frontend ============

@app.route('/')
def serve_index():
    """Serve React app index"""
    return send_from_directory('dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from React build"""
    if os.path.exists(os.path.join('dist', path)):
        return send_from_directory('dist', path)
    else:
        # Return index.html for client-side routing
        return send_from_directory('dist', 'index.html')

# ============ API Routes ============

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "app": "QuickAid Unified Application"})

# Emergency Contacts
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = db.fetchall("SELECT * FROM emergency_contacts ORDER BY is_primary DESC")
    return jsonify([dict(c) for c in contacts])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    db.execute('''
        INSERT INTO emergency_contacts (name, phone, category, relationship, address, is_primary, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data.get('name'), data.get('phone'), data.get('category', 'Personal'),
          data.get('relationship', ''), data.get('address', ''), data.get('is_primary', 0), data.get('notes', '')))
    return jsonify({"success": True, "message": "Contact added"}), 201

@app.route('/api/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    db.execute('''
        UPDATE emergency_contacts SET name=?, phone=?, category=?, relationship=?, notes=?
        WHERE id=?
    ''', (data.get('name'), data.get('phone'), data.get('category'),
          data.get('relationship'), data.get('notes'), contact_id))
    return jsonify({"success": True})

@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    db.execute("DELETE FROM emergency_contacts WHERE id = ?", (contact_id,))
    return jsonify({"success": True})

# First Aid Kit Items
@app.route('/api/first-aid-items', methods=['GET'])
def get_first_aid_items():
    items = db.fetchall("SELECT * FROM first_aid_kit_items ORDER BY name")
    return jsonify([dict(i) for i in items])

@app.route('/api/first-aid-items', methods=['POST'])
def add_first_aid_item():
    data = request.json
    db.execute('''
        INSERT INTO first_aid_kit_items (name, category, quantity, min_quantity, in_stock, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data.get('name'), data.get('category', 'General'), data.get('quantity', 1),
          data.get('min_quantity', 1), data.get('in_stock', 1), data.get('notes', '')))
    return jsonify({"success": True}), 201

@app.route('/api/first-aid-items/<item_id>', methods=['PUT'])
def update_first_aid_item(item_id):
    data = request.json
    db.execute('''
        UPDATE first_aid_kit_items SET name=?, quantity=?, in_stock=?, notes=?
        WHERE id=?
    ''', (data.get('name'), data.get('quantity'), data.get('in_stock'), data.get('notes'), item_id))
    return jsonify({"success": True})

@app.route('/api/first-aid-items/<item_id>', methods=['DELETE'])
def delete_first_aid_item(item_id):
    db.execute("DELETE FROM first_aid_kit_items WHERE id = ?", (item_id,))
    return jsonify({"success": True})

# Quiz
@app.route('/api/quiz/questions', methods=['GET'])
def get_quiz_questions():
    category = request.args.get('category')
    if category:
        filtered = [q for q in quiz_questions if q['category'] == category]
        return jsonify(filtered)
    return jsonify(quiz_questions)

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    data = request.json
    db.execute('''
        INSERT INTO quiz_scores (category, score, total_questions, percentage)
        VALUES (?, ?, ?, ?)
    ''', (data.get('category'), data.get('score'), data.get('total'),
          (data.get('score', 0) / max(data.get('total', 1), 1)) * 100))
    return jsonify({"success": True}), 201

@app.route('/api/quiz/results', methods=['GET'])
def get_quiz_results():
    results = db.fetchall("SELECT * FROM quiz_scores ORDER BY completed_at DESC LIMIT 10")
    return jsonify([dict(r) for r in results])

# Body Parts
@app.route('/api/body-parts', methods=['GET'])
def get_body_parts():
    parts = db.fetchall("SELECT * FROM body_parts")
    result = {}
    for part in parts:
        result[part['part_name'].lower()] = {
            "name": part['part_name'],
            "location": part['location'],
            "common_injuries": json.loads(part['common_injuries']) if part['common_injuries'] else [],
            "causes": json.loads(part['causes']) if part['causes'] else [],
            "symptoms": json.loads(part['symptoms']) if part['symptoms'] else [],
            "first_aid": json.loads(part['first_aid']) if part['first_aid'] else [],
        }
    return jsonify(result)

@app.route('/api/body-parts/<part_id>', methods=['GET'])
def get_body_part(part_id):
    part = db.fetchone("SELECT * FROM body_parts WHERE part_name = ? OR part_name = ?",
                       (part_id.capitalize(), part_id))
    if part:
        return jsonify({
            "name": part['part_name'],
            "location": part['location'],
            "common_injuries": json.loads(part['common_injuries']) if part['common_injuries'] else [],
            "causes": json.loads(part['causes']) if part['causes'] else [],
            "symptoms": json.loads(part['symptoms']) if part['symptoms'] else [],
            "first_aid": json.loads(part['first_aid']) if part['first_aid'] else [],
            "dos": json.loads(part['dos']) if part['dos'] else [],
            "donts": json.loads(part['donts']) if part['donts'] else [],
            "recovery_tips": json.loads(part['recovery_tips']) if part['recovery_tips'] else [],
            "warning_signs": json.loads(part['warning_signs']) if part['warning_signs'] else [],
        })
    return jsonify({"error": "Body part not found"}), 404

# Emergency Workflows
@app.route('/api/emergencies', methods=['GET'])
def get_emergencies():
    return jsonify(emergency_workflows)

@app.route('/api/emergencies/<emergency_type>', methods=['GET'])
def get_emergency(emergency_type):
    emergency = emergency_workflows.get(emergency_type)
    if emergency:
        return jsonify(emergency)
    return jsonify({"error": "Emergency type not found"}), 404

# First Aid Guides
@app.route('/api/first-aid-guides', methods=['GET'])
def get_first_aid_guides():
    guides = db.fetchall("SELECT * FROM first_aid_guides ORDER BY condition_name")
    result = []
    for g in guides:
        result.append({
            "id": g['id'],
            "name": g['condition_name'],
            "category": g['category'],
            "severity": g['severity'],
            "definition": g['definition'],
            "symptoms": json.loads(g['symptoms']) if g['symptoms'] else [],
            "immediate_action": g['immediate_action'],
            "steps": json.loads(g['step_by_step']) if g['step_by_step'] else [],
            "dos": json.loads(g['dos']) if g['dos'] else [],
            "donts": json.loads(g['donts']) if g['donts'] else [],
            "recovery": json.loads(g['recovery']) if g['recovery'] else [],
        })
    return jsonify(result)

@app.route('/api/first-aid-guides/<condition>', methods=['GET'])
def get_first_aid_guide(condition):
    guide = db.fetchone("SELECT * FROM first_aid_guides WHERE condition_name = ?", (condition,))
    if guide:
        return jsonify({
            "name": guide['condition_name'],
            "category": guide['category'],
            "severity": guide['severity'],
            "definition": guide['definition'],
            "symptoms": json.loads(guide['symptoms']) if guide['symptoms'] else [],
            "immediate_action": guide['immediate_action'],
            "steps": json.loads(guide['step_by_step']) if guide['step_by_step'] else [],
            "dos": json.loads(guide['dos']) if guide['dos'] else [],
            "donts": json.loads(guide['donts']) if guide['donts'] else [],
            "recovery": json.loads(guide['recovery']) if guide['recovery'] else [],
        })
    return jsonify({"error": "Guide not found"}), 404

# Preparedness Guides
@app.route('/api/preparedness', methods=['GET'])
def get_preparedness():
    return jsonify(preparedness_guides)

@app.route('/api/preparedness/<guide_id>', methods=['GET'])
def get_preparedness_guide(guide_id):
    guide = preparedness_guides.get(guide_id)
    if guide:
        return jsonify(guide)
    return jsonify({"error": "Guide not found"}), 404

# Symptoms
@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    symptoms = db.fetchall("SELECT * FROM symptoms ORDER BY name")
    return jsonify([dict(s) for s in symptoms])

# Medicines
@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    medicines = db.fetchall("SELECT * FROM medicines ORDER BY name")
    result = []
    for m in medicines:
        result.append({
            "id": m['id'],
            "name": m['name'],
            "generic_name": m['generic_name'],
            "category": m['category'],
            "uses": m['uses'],
            "dosage": m['dosage'],
            "adult_dosage": m['adult_dosage'],
            "child_dosage": m['child_dosage'],
            "side_effects": json.loads(m['side_effects']) if m['side_effects'] else [],
            "warnings": json.loads(m['warnings']) if m['warnings'] else [],
        })
    return jsonify(result)

# Medical Dictionary
@app.route('/api/dictionary', methods=['GET'])
def get_dictionary():
    terms = db.fetchall("SELECT * FROM medical_dictionary ORDER BY term")
    return jsonify([dict(t) for t in terms])

@app.route('/api/dictionary/search', methods=['GET'])
def search_dictionary():
    query = request.args.get('q', '').lower()
    terms = db.fetchall("SELECT * FROM medical_dictionary WHERE lower(term) LIKE ?",
                       (f'%{query}%',))
    return jsonify([dict(t) for t in terms])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"\n{'='*50}")
    print("Quick Aid - Smart First Aid & Emergency Care System")
    print(f"{'='*50}")
    print(f"\nApplication running at: http://localhost:{port}")
    print("Press Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=port, debug=False)
