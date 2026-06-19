-- Emergency Contacts Table
CREATE TABLE emergency_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    relationship TEXT NOT NULL,
    phone TEXT NOT NULL,
    is_favorite BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- First Aid Kit Items Table
CREATE TABLE first_aid_kit_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    item_name TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    is_available BOOLEAN DEFAULT false,
    last_checked TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quiz Questions Table
CREATE TABLE quiz_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    difficulty TEXT DEFAULT 'medium',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quiz Progress Table
CREATE TABLE quiz_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    score INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, category)
);

-- User Preferences Table
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
    large_text_mode BOOLEAN DEFAULT false,
    high_contrast_mode BOOLEAN DEFAULT false,
    voice_guidance_enabled BOOLEAN DEFAULT false,
    dark_mode BOOLEAN DEFAULT true,
    emergency_sms_template TEXT DEFAULT 'EMERGENCY! I need help immediately. This is an automated emergency alert from QuickAid.',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert Default Quiz Questions
INSERT INTO quiz_questions (category, question, option_a, option_b, option_c, option_d, correct_answer, explanation, difficulty) VALUES
('burns', 'What is the first thing you should do for a minor burn?', 'Apply ice directly', 'Run cool water over it', 'Apply butter or oil', 'Pop any blisters', 'option_b', 'Cool water helps reduce temperature and prevents further tissue damage. Never use ice, butter, or oil as they can worsen the injury.', 'easy'),
('burns', 'How long should you cool a burn under running water?', '30 seconds', '2 minutes', '10-20 minutes', '1 hour', 'option_c', 'Cooling a burn for 10-20 minutes under running water helps reduce pain and prevent further damage to the skin.', 'medium'),
('choking', 'What is the first step when someone is choking but can still cough?', 'Perform abdominal thrusts', 'Encourage them to cough', 'Give them water', 'Slap their back hard', 'option_b', 'If the person can still cough, they are still able to breathe. Encourage coughing as it is the most effective way to clear the obstruction.', 'easy'),
('choking', 'How many back blows should you give to a choking adult before abdominal thrusts?', '1', '3', '5', '10', 'option_c', 'Give 5 back blows between the shoulder blades, then 5 abdominal thrusts if the obstruction is not cleared.', 'medium'),
('bleeding', 'What is the correct way to control severe bleeding?', 'Apply direct pressure with clean cloth', 'Wash with water', 'Apply a tourniquet immediately', 'Let it bleed to clean wound', 'option_a', 'Direct pressure with a clean cloth is the first and most effective method to control bleeding. Elevate the limb if possible.', 'easy'),
('bleeding', 'When should a tourniquet be applied?', 'For any bleeding wound', 'Only for severe, life-threatening bleeding on limbs', 'For all head wounds', 'Never, it is dangerous', 'option_b', 'Tourniquets should only be used as a last resort for severe, life-threatening bleeding on limbs when direct pressure fails.', 'hard'),
('fractures', 'What should you do if you suspect a fracture?', 'Try to straighten the bone', 'Move the person immediately', 'Immobilize the area and seek medical help', 'Apply heat to reduce pain', 'option_c', 'Never try to straighten or move a suspected fracture. Immobilize the area to prevent further injury and seek immediate medical attention.', 'easy'),
('fractures', 'What is the correct way to immobilize a fractured limb?', 'Use a splint on both sides', 'Just wrap with bandage', 'Move it to a comfortable position', 'Apply ice directly', 'option_a', 'A splint should be applied on both sides of the fracture to provide support and prevent movement. Pad it well before applying.', 'medium'),
('electric_shock', 'What is the first step in helping someone with an electric shock?', 'Touch them to pull them away', 'Turn off the power source', 'Pour water on them', 'Call emergency services first', 'option_b', 'Always turn off the power source first. Never touch the person directly as you may also get shocked.', 'easy'),
('electric_shock', 'What should you use to separate a victim from an electrical source?', 'Your bare hands', 'A wet cloth', 'A dry wooden object', 'A metal rod', 'option_c', 'Use a dry, non-conductive object like wood to safely separate the victim from the electrical source.', 'medium'),
('heart_attack', 'What is a common symptom of a heart attack?', 'Chest pain or pressure', 'Stomach ache only', 'Headache', 'Sore throat', 'option_a', 'Chest pain, pressure, or squeezing sensation is the most common symptom of a heart attack. Pain may also radiate to the arm, jaw, or back.', 'easy'),
('heart_attack', 'What should you do if someone is having a heart attack?', 'Make them walk around', 'Have them sit and rest, call emergency', 'Give them food and water', 'Wait to see if it passes', 'option_b', 'Have the person sit in a comfortable position, remain calm, and call emergency services immediately. Time is critical in heart attacks.', 'medium'),
('cpr', 'What is the correct ratio of chest compressions to breaths for adult CPR?', '15:2', '30:2', '10:1', '20:3', 'option_b', 'For adult CPR, perform 30 chest compressions followed by 2 rescue breaths. This is the standard ratio recommended by medical guidelines.', 'medium'),
('cpr', 'How deep should chest compressions be for an adult?', '1 inch', '2 inches (5 cm)', '4 inches', 'As deep as possible', 'option_b', 'Chest compressions should be at least 2 inches (5 cm) deep for adults. This ensures adequate blood circulation.', 'medium'),
('stroke', 'What does F.A.S.T. stand for in stroke recognition?', 'Face, Arms, Speech, Time', 'Fast, Alert, Strong, Tall', 'Force, Action, Speed, Talk', 'First Aid, Safety, Treatment', 'option_a', 'F.A.S.T. helps identify stroke: Face (drooping), Arms (weakness), Speech (slurred), Time (call emergency immediately).', 'easy'),
('stroke', 'If you suspect someone is having a stroke, what should you do?', 'Wait to see if symptoms improve', 'Give them aspirin', 'Call emergency services immediately', 'Make them lie flat', 'option_c', 'Time is critical for stroke treatment. Call emergency services immediately. Do not give aspirin as it may worsen certain types of stroke.', 'medium'),
('drowning', 'What should you do first if someone is drowning?', 'Jump in immediately', 'Reach or throw something to help', 'Swim to them', 'Call their name loudly', 'option_b', 'Reach out with a pole, throw a rope or flotation device. Only enter the water as a last resort if you are trained to do so.', 'medium'),
('drowning', 'After rescuing a drowning person, what should you check first?', 'For injuries', 'Breathing and pulse', 'For water in lungs', 'Body temperature', 'option_b', 'Check if the person is breathing and has a pulse. Begin CPR if necessary. Call emergency services immediately.', 'hard'),
('snake_bite', 'What should you do for a snake bite?', 'Cut the wound and suck out venom', 'Apply a tight tourniquet', 'Keep the person calm and still, seek medical help', 'Apply ice to the bite', 'option_c', 'Keep the victim calm and still, immobilize the bitten area, and seek immediate medical help. Do not cut, suck, or apply tourniquets.', 'medium'),
('snake_bite', 'What information should you try to remember about a snake bite?', 'The snakes favorite food', 'The snakes color and pattern', 'The snakes age', 'The snakes name', 'option_b', 'Try to remember the snake is appearance (color, pattern, size) to help medical staff provide the correct antivenom if needed.', 'easy'),
('general', 'What is the universal emergency number in India?', '911', '112', '999', '100', 'option_b', '112 is the single emergency number in India for police, fire, and ambulance services.', 'easy'),
('general', 'What should be included in a first aid kit?', 'Prescription medications', 'Antiseptic and bandages', 'Sharp knives', 'Alcoholic beverages', 'option_b', 'A basic first aid kit should include antiseptic, bandages, gauze, adhesive tape, scissors, gloves, and basic medications.', 'easy');

-- Enable RLS
ALTER TABLE emergency_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE first_aid_kit_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- RLS Policies for emergency_contacts
CREATE POLICY "select_own_contacts" ON emergency_contacts FOR SELECT
    TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "insert_own_contacts" ON emergency_contacts FOR INSERT
    TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "update_own_contacts" ON emergency_contacts FOR UPDATE
    TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "delete_own_contacts" ON emergency_contacts FOR DELETE
    TO authenticated USING (auth.uid() = user_id);

-- RLS Policies for first_aid_kit_items
CREATE POLICY "select_own_kit_items" ON first_aid_kit_items FOR SELECT
    TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "insert_own_kit_items" ON first_aid_kit_items FOR INSERT
    TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "update_own_kit_items" ON first_aid_kit_items FOR UPDATE
    TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "delete_own_kit_items" ON first_aid_kit_items FOR DELETE
    TO authenticated USING (auth.uid() = user_id);

-- RLS Policies for quiz_progress
CREATE POLICY "select_own_progress" ON quiz_progress FOR SELECT
    TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "insert_own_progress" ON quiz_progress FOR INSERT
    TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "update_own_progress" ON quiz_progress FOR UPDATE
    TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- RLS Policies for user_preferences
CREATE POLICY "select_own_preferences" ON user_preferences FOR SELECT
    TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "insert_own_preferences" ON user_preferences FOR INSERT
    TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "update_own_preferences" ON user_preferences FOR UPDATE
    TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- Public read for quiz questions
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "select_quiz_questions" ON quiz_questions FOR SELECT
    TO authenticated USING (true);