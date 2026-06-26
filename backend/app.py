from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
CORS(app)

# In-memory storage for demo (replace with Supabase in production)
emergency_contacts = []
first_aid_items = []
quiz_results = []

# Quiz Questions Data
quiz_questions = [
    {"id": 1, "category": "burns", "question": "What is the first thing you should do for a minor burn?", "options": ["Apply ice directly", "Run cool water over it", "Apply butter or oil", "Pop any blisters"], "correct": 1, "explanation": "Cool water helps reduce temperature and prevents further tissue damage.", "difficulty": "easy"},
    {"id": 2, "category": "burns", "question": "How long should you cool a burn under running water?", "options": ["30 seconds", "2 minutes", "10-20 minutes", "1 hour"], "correct": 2, "explanation": "Cooling a burn for 10-20 minutes helps reduce pain and prevent further damage.", "difficulty": "medium"},
    {"id": 3, "category": "choking", "question": "What is the first step when someone is choking but can still cough?", "options": ["Perform abdominal thrusts", "Encourage them to cough", "Give them water", "Slap their back hard"], "correct": 1, "explanation": "If the person can still cough, encourage coughing to clear the obstruction.", "difficulty": "easy"},
    {"id": 4, "category": "choking", "question": "How many back blows should you give to a choking adult?", "options": ["1", "3", "5", "10"], "correct": 2, "explanation": "Give 5 back blows between the shoulder blades.", "difficulty": "medium"},
    {"id": 5, "category": "bleeding", "question": "What is the correct way to control severe bleeding?", "options": ["Apply direct pressure with clean cloth", "Wash with water", "Apply a tourniquet immediately", "Let it bleed to clean wound"], "correct": 0, "explanation": "Direct pressure with a clean cloth is the most effective method.", "difficulty": "easy"},
    {"id": 6, "category": "fractures", "question": "What should you do if you suspect a fracture?", "options": ["Try to straighten the bone", "Move the person immediately", "Immobilize the area and seek medical help", "Apply heat to reduce pain"], "correct": 2, "explanation": "Never try to straighten a fracture. Immobilize and seek medical attention.", "difficulty": "easy"},
    {"id": 7, "category": "electric_shock", "question": "What is the first step in helping someone with an electric shock?", "options": ["Touch them to pull them away", "Turn off the power source", "Pour water on them", "Call emergency services first"], "correct": 1, "explanation": "Always turn off the power source first. Never touch the person directly.", "difficulty": "easy"},
    {"id": 8, "category": "cpr", "question": "What is the correct ratio of chest compressions to breaths for adult CPR?", "options": ["15:2", "30:2", "10:1", "20:3"], "correct": 1, "explanation": "Perform 30 chest compressions followed by 2 rescue breaths.", "difficulty": "medium"},
    {"id": 9, "category": "stroke", "question": "What does F.A.S.T. stand for in stroke recognition?", "options": ["Face, Arms, Speech, Time", "Fast, Alert, Strong, Tall", "Force, Action, Speed, Talk", "First Aid, Safety, Treatment"], "correct": 0, "explanation": "F.A.S.T. helps identify stroke: Face drooping, Arms weakness, Speech slurred, Time to call emergency.", "difficulty": "easy"},
    {"id": 10, "category": "general", "question": "What should be included in a first aid kit?", "options": ["Prescription medications", "Antiseptic and bandages", "Sharp knives", "Alcoholic beverages"], "correct": 1, "explanation": "A basic first aid kit should include antiseptic, bandages, gauze, and gloves.", "difficulty": "easy"},
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

# ============ API Routes ============

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "app": "QuickAid Backend"})

# Emergency Contacts
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(emergency_contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contact = {
        "id": len(emergency_contacts) + 1,
        "name": data.get('name', ''),
        "relationship": data.get('relationship', ''),
        "phone": data.get('phone', ''),
        "is_primary": data.get('is_primary', False)
    }
    emergency_contacts.append(contact)
    return jsonify(contact), 201

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    for contact in emergency_contacts:
        if contact['id'] == contact_id:
            contact.update(data)
            return jsonify(contact)
    return jsonify({"error": "Contact not found"}), 404

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    global emergency_contacts
    emergency_contacts = [c for c in emergency_contacts if c['id'] != contact_id]
    return jsonify({"message": "Contact deleted"}), 200

# First Aid Kit Items
@app.route('/api/first-aid-items', methods=['GET'])
def get_first_aid_items():
    return jsonify(first_aid_items)

@app.route('/api/first-aid-items', methods=['POST'])
def add_first_aid_item():
    data = request.json
    item = {
        "id": len(first_aid_items) + 1,
        "name": data.get('name', ''),
        "quantity": data.get('quantity', 1),
        "in_stock": data.get('in_stock', True),
        "notes": data.get('notes', '')
    }
    first_aid_items.append(item)
    return jsonify(item), 201

@app.route('/api/first-aid-items/<int:item_id>', methods=['PUT'])
def update_first_aid_item(item_id):
    data = request.json
    for item in first_aid_items:
        if item['id'] == item_id:
            item.update(data)
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/first-aid-items/<int:item_id>', methods=['DELETE'])
def delete_first_aid_item(item_id):
    global first_aid_items
    first_aid_items = [i for i in first_aid_items if i['id'] != item_id]
    return jsonify({"message": "Item deleted"}), 200

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
    result = {
        "id": len(quiz_results) + 1,
        "category": data.get('category', ''),
        "score": data.get('score', 0),
        "total": data.get('total', 0),
        "answers": data.get('answers', [])
    }
    quiz_results.append(result)
    return jsonify(result), 201

@app.route('/api/quiz/results', methods=['GET'])
def get_quiz_results():
    return jsonify(quiz_results)

# Body Map
@app.route('/api/body-parts', methods=['GET'])
def get_body_parts():
    return jsonify(body_parts)

@app.route('/api/body-parts/<part_id>', methods=['GET'])
def get_body_part(part_id):
    part = body_parts.get(part_id)
    if part:
        return jsonify(part)
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port, debug=True)
