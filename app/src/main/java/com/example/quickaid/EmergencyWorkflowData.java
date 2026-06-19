package com.example.quickaid;

import com.example.quickaid.models.EmergencyWorkflow;

import java.util.Arrays;

public class EmergencyWorkflowData {

    public static EmergencyWorkflow getWorkflow(String type) {
        switch (type) {
            case "road_accident": return getRoadAccident();
            case "burns": return getBurns();
            case "electric_shock": return getElectricShock();
            case "fractures": return getFractures();
            case "choking": return getChoking();
            case "drowning": return getDrowning();
            case "snake_bite": return getSnakeBite();
            case "dog_bite": return getDogBite();
            case "heart_attack": return getHeartAttack();
            case "stroke": return getStroke();
            case "heat_stroke": return getHeatStroke();
            case "food_poisoning": return getFoodPoisoning();
            case "seizures": return getSeizures();
            case "unconscious": return getUnconscious();
            case "heavy_bleeding": return getHeavyBleeding();
            default: return getRoadAccident();
        }
    }

    private static EmergencyWorkflow getRoadAccident() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Road Accident", "🚗", "Immediate response to traffic accidents", 4);
        wf.setSymptoms(Arrays.asList(
            "Visible bleeding wounds",
            "Broken bones / deformity",
            "Loss of consciousness",
            "Severe pain",
            "Difficulty breathing",
            "Head injury / confusion"
        ));
        wf.setSteps(Arrays.asList(
            "Check scene safety before approaching",
            "Call 112 / 108 immediately for ambulance",
            "Do NOT move victim unless in immediate danger",
            "Check if victim is conscious and breathing",
            "Stop any severe bleeding by applying firm pressure with clean cloth",
            "If unconscious but breathing, place in recovery position",
            "If not breathing, begin CPR if trained",
            "Keep victim calm and warm until help arrives",
            "Monitor and note any changes in condition"
        ));
        wf.setDos(Arrays.asList(
            "Stay calm and call emergency services",
            "Apply gentle pressure to bleeding wounds",
            "Support broken limbs gently without moving them",
            "Keep victim warm and comfortable",
            "Note what happened for emergency responders"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT move victim with suspected spine injury",
            "Do NOT remove helmet if worn",
            "Do NOT straighten broken bones",
            "Do NOT give food or water to unconscious person",
            "Do NOT crowd around the victim"
        ));
        wf.setWhenToCallEmergency("ALWAYS call 112 immediately for any road accident with injuries.");
        return wf;
    }

    private static EmergencyWorkflow getBurns() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Burns", "🔥", "Treatment for thermal burns", 2);
        wf.setSymptoms(Arrays.asList(
            "Red or peeling skin",
            "Pain or burning sensation",
            "Blisters formation",
            "Swelling",
            "Charred skin (severe burns)"
        ));
        wf.setSteps(Arrays.asList(
            "Remove from heat source immediately",
            "Cool burn under cool running water for 10-20 minutes",
            "Remove jewelry and tight items near the burn",
            "Cover burns loosely with clean, non-fluffy cloth",
            "Do NOT break any blisters",
            "Keep the person warm (avoid chilling)",
            "Elevate burned area if possible",
            "For severe burns, call 112 immediately"
        ));
        wf.setDos(Arrays.asList(
            "Use cool/room temperature water",
            "Cover with clean cloth loosely",
            "Seek medical help for severe burns",
            "Keep burn area elevated",
            "Stay calm"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT use ice or ice water",
            "Do NOT apply toothpaste, butter, or oil",
            "Do NOT break blisters",
            "Do NOT remove stuck clothing",
            "Do NOT touch burn with dirty hands"
        ));
        wf.setWhenToCallEmergency("Call 112 if: burn covers large area, electrical/chemical burn, facial burn, difficulty breathing, or third-degree burn.");
        return wf;
    }

    private static EmergencyWorkflow getElectricShock() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Electric Shock", "⚡", "Emergency response to electrical injuries", 4);
        wf.setSymptoms(Arrays.asList(
            "Visible burns at entry/exit points",
            "Muscle spasms/pain",
            "Difficulty breathing",
            "Irregular heartbeat",
            "Unconsciousness",
            "Cardiac arrest possible"
        ));
        wf.setSteps(Arrays.asList(
            "Do NOT touch victim until power is off",
            "Switch off power at source or circuit breaker",
            "If unable to turn off, use dry wood/rubber to separate victim from source",
            "Once safe, check consciousness and breathing",
            "If not breathing, begin CPR immediately",
            "Call 112 IMMEDIATELY - electrical injuries are always serious",
            "Treat visible burns with cool water",
            "Keep victim still and calm"
        ));
        wf.setDos(Arrays.asList(
            "Turn off power FIRST",
            "Use non-conductive objects if needed",
            "Call emergency services immediately",
            "Begin CPR if needed",
            "Monitor breathing continuously"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT touch victim while in contact with power",
            "Do NOT use wet hands or objects",
            "Do NOT touch victim's body directly if power still on",
            "Do NOT pour water on electrical source",
            "Do NOT move victim unnecessarily"
        ));
        wf.setWhenToCallEmergency("ALWAYS call 112 for any electrical shock - internal damage may not be visible.");
        return wf;
    }

    private static EmergencyWorkflow getFractures() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Fractures", "🦴", "Bone fracture emergency care", 3);
        wf.setSymptoms(Arrays.asList(
            "Intense pain at injury site",
            "Swelling and bruising",
            "Visible deformity",
            "Inability to move affected area",
            "Bone visible through skin (open fracture)",
            "Tenderness to touch"
        ));
        wf.setSteps(Arrays.asList(
            "Keep the person still and calm",
            "Do NOT try to straighten the bone",
            "Immobilize the injured area - use splints if available",
            "Apply ice wrapped in cloth to reduce swelling",
            "Elevate the injured area if possible",
            "For open fracture, cover wound with clean cloth",
            "Call 108 for ambulance or transport carefully",
            "Monitor for shock symptoms"
        ));
        wf.setDos(Arrays.asList(
            "Immobilize with makeshift splint",
            "Pad the splint for comfort",
            "Apply ice (wrapped) for swelling",
            "Elevate if possible",
            "Seek medical attention promptly"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT attempt to straighten bone",
            "Do NOT move the broken bone",
            "Do NOT push bone back if protruding",
            "Do NOT give food/water (may need surgery)",
            "Do NOT massage the area"
        ));
        wf.setWhenToCallEmergency("Call 112 if: bone visible, limb looks deformed, severe bleeding, possible spine injury.");
        return wf;
    }

    private static EmergencyWorkflow getChoking() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Choking", "😮", "Airway obstruction emergency", 4);
        wf.setSymptoms(Arrays.asList(
            "Difficulty breathing or noisy breathing",
            "Unable to speak or cry",
            "Clutching throat",
            "Blue lips or face (cyanosis)",
            "Loss of consciousness",
            "Weak or absent cough"
        ));
        wf.setSteps(Arrays.asList(
            "If person can cough, encourage them to continue coughing",
            "If cannot cough, talk, or breathe - act immediately",
            "Give 5 firm back blows between shoulder blades",
            "If still choking, give 5 abdominal thrusts (Heimlich maneuver)",
            "Alternate between 5 back blows and 5 thrusts",
            "If unconscious, lower to ground and begin CPR",
            "Call 112 if obstruction not cleared quickly"
        ));
        wf.setDos(Arrays.asList(
            "Act quickly - seconds matter",
            "Encourage coughing if effective",
            "Use proper hand position for thrusts",
            "Call for help immediately",
            "Be prepared for CPR"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT give water while choking",
            "Do NOT put fingers blindly in mouth",
            "Do NOT slap on the back if person upright",
            "Do NOT wait too long to call help",
            "Do NOT perform thrusts on infants like adults"
        ));
        wf.setWhenToCallEmergency("Call 112 immediately if: complete blockage, person loses consciousness, abdominal thrusts fail.");
        return wf;
    }

    private static EmergencyWorkflow getDrowning() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Drowning", "🌊", "Water rescue and resuscitation", 4);
        wf.setSymptoms(Arrays.asList(
            "Person in water calling for help or silent",
            "Head low in water, mouth at water level",
            "Arms moving up and down (climbing ladder)",
            "Gasping for air",
            "Blue-tinged skin",
            "Unconscious in water"
        ));
        wf.setSteps(Arrays.asList(
            "Call for help and throw flotation device if possible",
            "Reach with pole or branch - DO NOT enter unless trained",
            "If trained, approach from behind",
            "Once rescued, check for breathing immediately",
            "If not breathing, begin CPR immediately",
            "If breathing, place in recovery position",
            "Keep person warm and monitor for hypothermia",
            "ALL drowning victims should see a doctor"
        ));
        wf.setDos(Arrays.asList(
            "Reach, throw, row, go - in that order",
            "Begin CPR immediately if not breathing",
            "Keep rescue simple and safe",
            "Call 112 immediately",
            "Monitor for secondary drowning"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT jump in unless trained and necessary",
            "Do NOT let victim grab you directly",
            "Do NOT delay CPR",
            "Do NOT assume person is OK after rescue",
            "Do NOT give up on CPR too early"
        ));
        wf.setWhenToCallEmergency("ALWAYS seek medical attention for drowning victims - delayed complications can occur.");
        return wf;
    }

    private static EmergencyWorkflow getSnakeBite() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Snake Bite", "🐍", "Snake envenomation emergency", 4);
        wf.setSymptoms(Arrays.asList(
            "Two puncture wounds",
            "Pain and swelling at bite site",
            "Nausea and vomiting",
            "Difficulty breathing",
            "Blurred vision",
            "Drowsiness or confusion"
        ));
        wf.setSteps(Arrays.asList(
            "Move away from the snake slowly",
            "Keep the person calm - panic increases venom spread",
            "Call 112 IMMEDIATELY",
            "Remove jewelry and tight items before swelling",
            "Keep bitten limb BELOW heart level",
            "Immobilize the limb with splint",
            "Note the time of bite and snake appearance if possible",
            "DO NOT attempt to catch the snake"
        ));
        wf.setDos(Arrays.asList(
            "Keep victim calm and still",
            "Immobilize bitten limb",
            "Keep limb below heart level",
            "Note time of bite",
            "Get to hospital immediately"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT cut the wound",
            "Do NOT suck out the venom",
            "Do NOT apply tourniquet",
            "Do NOT apply ice",
            "Do NOT drink alcohol or take painkillers"
        ));
        wf.setWhenToCallEmergency("ALWAYS call 112 for any snake bite. Antivenom treatment is critical.");
        return wf;
    }

    private static EmergencyWorkflow getDogBite() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Dog Bite", "🐕", "Animal bite wound management", 3);
        wf.setSymptoms(Arrays.asList(
            "Puncture wounds or lacerations",
            "Bleeding",
            "Pain and swelling",
            "Possible infection signs later",
            "Tissue damage"
        ));
        wf.setSteps(Arrays.asList(
            "Stop bleeding with clean cloth pressure",
            "Wash wound thoroughly with soap and water",
            "Apply antibiotic ointment if available",
            "Cover with clean bandage",
            "Check vaccination status - yours and the animal's",
            "Seek medical attention for deep wounds",
            "Report the incident to local authorities",
            "Watch for signs of infection"
        ));
        wf.setDos(Arrays.asList(
            "Clean wound thoroughly",
            "Apply pressure to stop bleeding",
            "Seek medical attention for deep wounds",
            "Get tetanus shot if needed",
            "Report stray dogs"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT ignore deep puncture wounds",
            "Do NOT close wound tightly - may need to drain",
            "Do NOT neglect vaccination follow-up",
            "Do NOT ignore infection signs",
            "Do NOT approach dogs showing rabies signs"
        ));
        wf.setWhenToCallEmergency("Call 112 if: severe bleeding, child attacked, wild/stray animal, signs of rabies.");
        return wf;
    }

    private static EmergencyWorkflow getHeartAttack() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Heart Attack", "❤️", "Acute myocardial infarction response", 4);
        wf.setSymptoms(Arrays.asList(
            "Chest pain/pressure/squeezing",
            "Pain radiating to arm, jaw, back",
            "Shortness of breath",
            "Cold sweat",
            "Nausea",
            "Feeling of impending doom"
        ));
        wf.setSteps(Arrays.asList(
            "Call 112 IMMEDIATELY - say 'heart attack'",
            "Have person sit down, stay calm",
            "Loosen tight clothing",
            "If prescribed, help person take nitroglycerin",
            "If no allergy, chew and swallow aspirin (325mg)",
            "Be prepared to perform CPR",
            "Do NOT leave person alone",
            "Note time of symptom onset"
        ));
        wf.setDos(Arrays.asList(
            "Call emergency immediately",
            "Keep person calm and sitting",
            "Give aspirin if no allergy",
            "Be ready for CPR",
            "Stay with patient until help arrives"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT drive yourself to hospital",
            "Do NOT delay calling for help",
            "Do NOT ignore 'mild' symptoms",
            "Do NOT give food or drink",
            "Do NOT leave person alone"
        ));
        wf.setWhenToCallEmergency("Call 112 IMMEDIATELY at first signs of heart attack. Every minute matters.");
        return wf;
    }

    private static EmergencyWorkflow getStroke() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Stroke", "🧠", "Brain attack emergency - Act FAST", 4);
        wf.setSymptoms(Arrays.asList(
            "Face drooping on one side",
            "Arm weakness - cannot raise both arms",
            "Speech difficulty or slurring",
            "Time critical - sudden onset",
            "Confusion",
            "Severe headache"
        ));
        wf.setSteps(Arrays.asList(
            "Recognize FAST: Face, Arms, Speech, Time",
            "Call 112 IMMEDIATELY - say 'stroke'",
            "Note time symptoms started",
            "Keep person comfortable, lying on side",
            "Do NOT give food, water, or medication",
            "Monitor breathing until help arrives",
            "Do NOT wait for symptoms to improve",
            "Stay calm and reassure the person"
        ));
        wf.setDos(Arrays.asList(
            "Act FAST - call immediately",
            "Note exact time of onset",
            "Keep person lying down comfortably",
            "Reassure and calm the person",
            "Have medical history ready"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT give any medication",
            "Do NOT give food or water",
            "Do NOT wait to see if it passes",
            "Do NOT drive - call ambulance",
            "Do NOT ignore even if symptoms improve"
        ));
        wf.setWhenToCallEmergency("Call 112 IMMEDIATELY if ANY stroke symptom. Treatment window is 3-4.5 hours.");
        return wf;
    }

    private static EmergencyWorkflow getHeatStroke() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Heat Stroke", "🌡️", "Heat-related emergency", 4);
        wf.setSymptoms(Arrays.asList(
            "High body temperature (40°C+)",
            "Hot, red, dry skin",
            "Confusion or altered behavior",
            "Rapid pulse",
            "Headache",
            "Nausea or vomiting",
            "Unconsciousness possible"
        ));
        wf.setSteps(Arrays.asList(
            "Move to cool, shaded area immediately",
            "Call 112",
            "Remove excess clothing",
            "Cool rapidly - wet skin, fan, ice packs to neck/armpits/groin",
            "If conscious, give cool water to sip",
            "Monitor body temperature",
            "Continue cooling until body temp drops",
            "Seek immediate medical attention"
        ));
        wf.setDos(Arrays.asList(
            "Cool body rapidly - this is critical",
            "Move to shade immediately",
            "Use water, fans, ice packs",
            "Call emergency services",
            "Monitor temperature if able"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT use alcohol rub",
            "Do NOT give medications for fever",
            "Do NOT leave unattended",
            "Do NOT give cold water if unconscious",
            "Do NOT pack in ice completely"
        ));
        wf.setWhenToCallEmergency("Call 112 for: unconsciousness, confusion, temperature above 40°C, seizures.");
        return wf;
    }

    private static EmergencyWorkflow getFoodPoisoning() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Food Poisoning", "🤢", "Foodborne illness management", 2);
        wf.setSymptoms(Arrays.asList(
            "Nausea and vomiting",
            "Diarrhea",
            "Abdominal cramps",
            "Fever",
            "Dehydration",
            "Weakness"
        ));
        wf.setSteps(Arrays.asList(
            "Stop eating if symptoms occur",
            "Sip small amounts of water or ORS",
            "Rest and allow stomach to settle",
            "Avoid solid foods initially",
            "Monitor for dehydration",
            "Eat bland foods when able (BRAT diet)",
            "Seek medical help if severe symptoms persists",
            "Keep sample if suspected contaminated food"
        ));
        wf.setDos(Arrays.asList(
            "Stay hydrated - sip frequently",
            "Use ORS if available",
            "Rest the digestive system",
            "Monitor for dehydration signs",
            "Seek help if symptoms severe"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT take anti-diarrheal immediately",
            "Do NOT eat solid foods too soon",
            "Do NOT ignore blood in stool",
            "Do NOT ignore high fever",
            "Do NOT give to others to eat suspect food"
        ));
        wf.setWhenToCallEmergency("Seek medical help if: blood in stool, high fever, severe dehydration, unable to keep liquids down.");
        return wf;
    }

    private static EmergencyWorkflow getSeizures() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Seizures", "⚡", "Seizure first aid", 3);
        wf.setSymptoms(Arrays.asList(
            "Uncontrolled muscle movements",
            "Loss of consciousness",
            "Confusion after event",
            "Possible tongue bite",
            "Loss of bladder control",
            "Staring spells (absence seizures)"
        ));
        wf.setSteps(Arrays.asList(
            "Stay calm and note start time",
            "Clear area of sharp objects",
            "Cushion head with something soft",
            "Turn person gently to side",
            "Do NOT restrain or hold down",
            "Do NOT put anything in mouth",
            "Time the seizure",
            "Stay until fully alert"
        ));
        wf.setDos(Arrays.asList(
            "Time the seizure",
            "Protect from injury",
            "Turn to side after seizure",
            "Stay calm and reassure",
            "Call 112 if first seizure or prolonged"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT hold person down",
            "Do NOT put anything in mouth",
            "Do NOT give food/water until fully alert",
            "Do NOT restrain movements",
            "Do NOT try to wake during seizure"
        ));
        wf.setWhenToCallEmergency("Call 112 if: first seizure, longer than 5 minutes, injury occurred, person pregnant.");
        return wf;
    }

    private static EmergencyWorkflow getUnconscious() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Unconscious Person", "😵", "Loss of consciousness response", 4);
        wf.setSymptoms(Arrays.asList(
            "No response to voice or touch",
            "Not moving voluntarily",
            "Possible abnormal breathing",
            "May have pale/blue skin",
            "Weak or absent pulse"
        ));
        wf.setSteps(Arrays.asList(
            "Check for safety and scene",
            "Call 112 IMMEDIATELY",
            "Check for response - tap shoulders, call name",
            "Open airway - tilt head back gently",
            "Look, listen, feel for breathing for 10 seconds",
            "If not breathing normally, start CPR",
            "If breathing, place in recovery position",
            "Monitor continuously until help arrives"
        ));
        wf.setDos(Arrays.asList(
            "Call 112 immediately",
            "Check for breathing",
            "Start CPR if needed",
            "Place in recovery position if breathing",
            "Continue monitoring"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT leave person alone",
            "Do NOT give food or water",
            "Do NOT shake or slap vigorously",
            "Do NOT assume person is OK if breathing",
            "Do NOT move unless necessary"
        ));
        wf.setWhenToCallEmergency("ALWAYS call 112 for any unconscious person. Time is critical.");
        return wf;
    }

    private static EmergencyWorkflow getHeavyBleeding() {
        EmergencyWorkflow wf = new EmergencyWorkflow(
            "Heavy Bleeding", "🩸", "Severe hemorrhage control", 4);
        wf.setSymptoms(Arrays.asList(
            "Blood flowing rapidly from wound",
            "Blood soaking through bandages",
            "Pale, cold skin",
            "Rapid, weak pulse",
            "Dizziness or confusion",
            "Shock symptoms"
        ));
        wf.setSteps(Arrays.asList(
            "Call 112 IMMEDIATELY",
            "Apply direct, firm pressure with clean cloth",
            "Do NOT remove the first pad - add more on top",
            "If possible, elevate the injured area above heart",
            "Press hard - body needs significant pressure",
            "If limb, consider tourniquet AS LAST RESORT only for life-threatening bleeding",
            "Keep person warm and lying down",
            "Monitor for shock signs until help arrives"
        ));
        wf.setDos(Arrays.asList(
            "Apply FIRM pressure continuously",
            "Elevate if possible",
            "Keep person calm and warm",
            "Call emergency immediately",
            "Be ready to help with shock"
        ));
        wf.setDonts(Arrays.asList(
            "Do NOT remove pressure",
            "Do NOT peek to check",
            "Do NOT use tourniquet unless life-threatening",
            "Do NOT give food or water",
            "Do NOT move unnecessarily"
        ));
        wf.setWhenToCallEmergency("Call 112 IMMEDIATELY for heavy bleeding that won't stop with direct pressure.");
        return wf;
    }
}
