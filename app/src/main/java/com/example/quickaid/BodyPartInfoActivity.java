package com.example.quickaid;

import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.utils.PreferencesManager;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class BodyPartInfoActivity extends AppCompatActivity {

    private TextView textViewTitle;
    private TextView textViewInjuries;
    private TextView textViewFirstAid;
    private TextView textViewPrecautions;
    private TextView textViewWarnings;
    private TextView textViewDonts;

    private TextToSpeech textToSpeech;
    private PreferencesManager preferencesManager;

    private static final Map<String, BodyPartInfo> BODY_DATA = new HashMap<>();

    static {
        BODY_DATA.put("head", new BodyPartInfo(
            "Head",
            "• Head injury / Concussion\n" +
            "• Headache / Migraine\n" +
            "• Lacerations / Cuts\n" +
            "• Skull fracture\n" +
            "• Traumatic brain injury",
            "1. Check consciousness and breathing\n" +
            "2. Apply gentle pressure to any bleeding\n" +
            "3. Keep person still and calm\n" +
            "4. Apply ice pack to swelling (wrapped)\n" +
            "5. Seek immediate medical help if:\n" +
            "   - Loss of consciousness\n" +
            "   - Vomiting\n" +
            "   - Severe headache\n" +
            "   - Confusion or dizziness",
            "• Always wear helmets during activities\n" +
            "• Use seat belts in vehicles\n" +
            "• Avoid dangerous stunts\n" +
            "• Keep surroundings safe",
            "⚠️ Call 112 immediately if:\n" +
            "• Person loses consciousness\n" +
            "• Clear fluid from ears/nose\n" +
            "• Unequal pupil size\n" +
            "• Severe bleeding\n" +
            "• Seizure occurs",
            "✘ Do NOT shake the person\n" +
            "✘ Do NOT remove any embedded objects\n" +
            "✘ Do NOT move unnecessarily\n" +
            "✘ Do NOT give food or water"
        ));

        BODY_DATA.put("eyes", new BodyPartInfo(
            "Eyes",
            "• Foreign object in eye\n" +
            "• Chemical burns\n" +
            "• Eye injury / Scratch\n" +
            "• Black eye\n" +
            "• Sudden vision loss",
            "1. For foreign object:\n" +
            "   - Do NOT rub\n" +
            "   - Try blinking repeatedly\n" +
            "   - Flush with clean water\n" +
            "2. For chemical exposure:\n" +
            "   - Flush with water for 15+ minutes\n" +
            "3. Cover injured eye loosely\n" +
            "4. Seek medical help immediately",
            "• Wear protective eyewear\n" +
            "• Use proper lighting\n" +
            "• Take breaks from screens\n" +
            "• Keep chemicals away",
            "⚠️ Seek emergency care if:\n" +
            "• Severe pain or vision loss\n" +
            "• Chemical exposure\n" +
            "• Penetrating injury\n" +
            "• Blood in the eye",
            "✘ Do NOT rub eyes\n" +
            "✘ Do NOT try to remove embedded objects\n" +
            "✘ Do NOT patch both eyes\n" +
            "✘ Do NOT use tap water for severe injuries"
        ));

        BODY_DATA.put("ears", new BodyPartInfo(
            "Ears",
            "• Foreign object in ear\n" +
            "• Ear infection\n" +
            "• Ear injury / Bleeding\n" +
            "• Hearing loss\n" +
            "• Ruptured eardrum",
            "1. For foreign object:\n" +
            "   - Do NOT try to remove with tools\n" +
            "   - Tilt head to let gravity help\n" +
            "   - Seek medical help if stuck\n" +
            "2. For injury:\n" +
            "   - Apply gentle pressure if bleeding\n" +
            "   - Keep ear dry\n" +
            "3. Seek medical attention",
            "• Keep ears dry and clean\n" +
            "• Avoid loud noises\n" +
            "• Don't insert objects\n" +
            "• Use ear protection",
            "⚠️ Seek help if:\n" +
            "• Severe pain\n" +
            "• Bleeding from ear\n" +
            "• Sudden hearing loss\n" +
            "• Fluid drainage",
            "✘ Do NOT use cotton swabs deep inside\n" +
            "✘ Do NOT use sharp objects\n" +
            "✘ Do NOT try to remove impacted objects\n" +
            "✘ do NOT ignore severe pain"
        ));

        BODY_DATA.put("neck", new BodyPartInfo(
            "Neck",
            "• Whiplash injury\n" +
            "• Neck strain / Sprain\n" +
            "• Cervical fracture\n" +
            "• Choking\n" +
            "• Cut / Laceration",
            "1. For neck injury/spine:\n" +
            "   - Do NOT move person\n" +
            "   - Keep head still\n" +
            "   - Call 112 immediately\n" +
            "2. For choking:\n" +
            "   - Perform Heimlich maneuver\n" +
            "3. For cuts:\n" +
            "   - Apply gentle pressure\n" +
            "   - Keep wound clean",
            "• Use proper posture\n" +
            "• Don't sleep on wrong pillow\n" +
            "• Exercise neck gently\n" +
            "• Wear helmets/seatbelts",
            "⚠️ IMMEDIATE EMERGENCY if:\n" +
            "• Cannot move arms/legs\n" +
            "• Severe pain after injury\n" +
            "• Difficulty breathing\n" +
            "• Loss of sensation",
            "✘ Do NOT move spine injury victim\n" +
            "✘ Do NOT twist neck\n" +
            "✘ Do NOT ignore numbness\n" +
            "✘ Do NOT massage severe injury"
        ));

        BODY_DATA.put("chest", new BodyPartInfo(
            "Chest / Heart",
            "• Heart attack\n" +
            "• Cardiac arrest\n" +
            "• Chest injury trauma\n" +
            "• Broken ribs\n" +
            "• Breathing difficulty",
            "1. For heart attack:\n" +
            "   - Call 112 immediately\n" +
            "   - Have person sit/rest\n" +
            "   - If prescribed, give aspirin\n" +
            "   - Be ready for CPR\n" +
            "2. For cardiac arrest:\n" +
            "   - Start CPR immediately\n" +
            "   - Use AED if available\n" +
            "3. For injury:\n" +
            "   - Apply pressure if bleeding",
            "• Regular exercise\n" +
            "• Healthy diet\n" +
            "• Avoid smoking\n" +
            "• Manage stress",
            "⚠️ CALL 112 IMMEDIATELY if:\n" +
            "• Chest pain/pressure\n" +
            "• Pain radiating to arm/jaw\n" +
            "• Shortness of breath\n" +
            "• Cold sweat\n" +
            "• Unconsciousness",
            "✘ Do NOT ignore chest pain\n" +
            "✘ Do NOT drive yourself\n" +
            "✘ Do NOT take too long to call help\n" +
            "✘ Do NOT pause CPR once started"
        ));

        BODY_DATA.put("abdomen", new BodyPartInfo(
            "Abdomen / Stomach",
            "• Abdominal injury/trauma\n" +
            "• Appendicitis signs\n" +
            "• Stomach pain\n" +
            "• Food poisoning\n" +
            "• Internal bleeding",
            "1. For abdominal trauma:\n" +
            "   - Do NOT apply pressure\n" +
            "   - Keep person still\n" +
            "   - Seek immediate help\n" +
            "2. For severe pain:\n" +
            "   - Note symptoms\n" +
            "   - Don't eat/drink\n" +
            "   - Seek medical help\n" +
            "3. For food poisoning:\n" +
            "   - Stay hydrated\n" +
            "   - Monitor symptoms",
            "• Eat healthy diet\n" +
            "• Avoid contaminated food\n" +
            "• Regular exercise\n" +
            "• Stay hydrated",
            "⚠️ Seek emergency care if:\n" +
            "• Severe abdominal pain\n" +
            "• Blood in stool/vomit\n" +
            "• Rigid/stiff abdomen\n" +
            "• Fever with pain\n" +
            "• Injury from impact",
            "✘ Do NOT apply heat\n" +
            "✘ Do NOT give painkillers\n" +
            "✘ Do NOT eat/drink if injury\n" +
            "✘ Do NOT press on abdomen"
        ));

        BODY_DATA.put("arm_left", new BodyPartInfo(
            "Arm / Left",
            "• Fracture / Broken bone\n" +
            "• Dislocation\n" +
            "• Sprain / Strain\n" +
            "• Cut / Laceration\n" +
            "• Arm pain / Heart related",
            "1. For fracture:\n" +
            "   - Immobilize arm\n" +
            "   - Apply splint\n" +
            "   - Apply ice wrapped in cloth\n" +
            "   - Seek medical help\n" +
            "2. For cuts:\n" +
            "   - Apply pressure\n" +
            "   - Clean and dress\n" +
            "3. Left arm pain may indicate heart attack",
            "• Warm up before exercise\n" +
            "• Use proper technique\n" +
            "• Wear protective gear\n" +
            "• Rest when tired",
            "⚠️ EMERGENCY if left arm pain with:\n" +
            "• Chest pain\n" +
            "• Shortness of breath\n" +
            "• Severe fracture\n" +
            "• Heavy bleeding",
            "✘ Do NOT move broken bone\n" +
            "✘ Do NOT straighten deformity\n" +
            "✘ Do NOT ignore heart signs\n" +
            "✘ Do NOT ignore severe swelling"
        ));

        BODY_DATA.put("arm_right", new BodyPartInfo(
            "Arm / Right",
            "• Fracture / Broken bone\n" +
            "• Dislocation\n" +
            "• Sprain / Strain\n" +
            "• Cut / Laceration\n" +
            "• Burns",
            "1. For fracture:\n" +
            "   - Immobilize arm\n" +
            "   - Apply splint\n" +
            "   - Apply ice wrapped in cloth\n" +
            "   - Seek medical help\n" +
            "2. For cuts:\n" +
            "   - Apply pressure\n" +
            "   - Clean and dress",
            "• Warm up before exercise\n" +
            "• Use proper technique\n" +
            "• Wear protective gear\n" +
            "• Rest when tired",
            "⚠️ Seek help if:\n" +
            "• Visible deformity\n" +
            "• Severe pain/swelling\n" +
            "• Loss of movement\n" +
            "• Heavy bleeding",
            "✘ Do NOT move broken bone\n" +
            "✘ Do NOT straighten deformity\n" +
            "✘ Do NOT ignore numbness\n" +
            "✘ Do NOT ignore severe swelling"
        ));

        BODY_DATA.put("hand_left", new BodyPartInfo(
            "Hand / Left",
            "• Finger cuts/burns\n" +
            "• Fractured fingers\n" +
            "• Jam/sprain\n" +
            "• Crush injury\n" +
            "• Foreign object",
            "1. For cuts:\n" +
            "   - Clean wound\n" +
            "   - Apply pressure\n" +
            "   - Bandage appropriately\n" +
            "2. For fracture:\n" +
            "   - Immobilize finger\n" +
            "   - Apply ice wrapped\n" +
            "   - Seek medical help",
            "• Use gloves when needed\n" +
            "• Be careful with tools\n" +
            "• Watch for hazards\n" +
            "• Keep nails trimmed",
            "⚠️ Seek help if:\n" +
            "• Severe bleeding\n" +
            "• Visible deformity\n" +
            "• Loss of movement\n" +
            "• Crush injury",
            "✘ Do NOT straighten broken finger\n" +
            "✘ Do NOT remove embedded objects\n" +
            "✘ Do NOT ignore numbness\n" +
            "✘ Do NOT wrap too tightly"
        ));

        BODY_DATA.put("hand_right", new BodyPartInfo(
            "Hand / Right",
            "• Finger cuts/burns\n" +
            "• Fractured fingers\n" +
            "• Jam/sprain\n" +
            "• Crush injury\n" +
            "• Foreign object",
            "1. For cuts:\n" +
            "   - Clean wound\n" +
            "   - Apply pressure\n" +
            "   - Bandage appropriately\n" +
            "2. For fracture:\n" +
            "   - Immobilize finger\n" +
            "   - Apply ice wrapped\n" +
            "   - Seek medical help",
            "• Use gloves when needed\n" +
            "• Be careful with tools\n" +
            "• Watch for hazards\n" +
            "• Keep nails trimmed",
            "⚠️ Seek help if:\n" +
            "• Severe bleeding\n" +
            "• Visible deformity\n" +
            "• Loss of movement\n" +
            "• Crush injury",
            "✘ Do NOT straighten broken finger\n" +
            "✘ Do NOT remove embedded objects\n" +
            "✘ Do NOT ignore numbness\n" +
            "✘ Do NOT wrap too tightly"
        ));

        BODY_DATA.put("leg_left", new BodyPartInfo(
            "Leg / Left",
            "• Fracture / Broken bone\n" +
            "• Dislocation\n" +
            "• Sprain / Strain\n" +
            "• Deep vein thrombosis\n" +
            "• Animal bite / Cut",
            "1. For fracture:\n" +
            "   - Do NOT move person\n" +
            "   - Immobilize leg with splint\n" +
            "   - Apply ice wrapped in cloth\n" +
            "   - Call for medical help\n" +
            "2. For sprain (RICE method):\n" +
            "   - Rest, Ice, Compression, Elevation\n" +
            "3. For cuts/bites:\n" +
            "   - Clean wound\n" +
            "   - Apply pressure",
            "• Warm up before exercise\n" +
            "• Wear proper footwear\n" +
            "• Stay active\n" +
            "• Maintain healthy weight",
            "⚠️ EMERGENCY if:\n" +
            "• Bone visible\n" +
            "• Severe deformity\n" +
            "• Heavy bleeding\n" +
            "• Cannot move leg\n" +
            "• Sudden swelling with pain",
            "✘ Do NOT move broken bone\n" +
            "✘ Do NOT straighten deformity\n" +
            "✘ Do NOT ignore blood clots\n" +
            "✘ Do NOT put weight on injury"
        ));

        BODY_DATA.put("leg_right", new BodyPartInfo(
            "Leg / Right",
            "• Fracture / Broken bone\n" +
            "• Dislocation\n" +
            "• Sprain / Strain\n" +
            "• Deep vein thrombosis\n" +
            "• Animal bite / Cut",
            "1. For fracture:\n" +
            "   - Do NOT move person\n" +
            "   - Immobilize leg with splint\n" +
            "   - Apply ice wrapped in cloth\n" +
            "   - Call for medical help\n" +
            "2. For sprain (RICE method):\n" +
            "   - Rest, Ice, Compression, Elevation",
            "• Warm up before exercise\n" +
            "• Wear proper footwear\n" +
            "• Stay active\n" +
            "• Maintain healthy weight",
            "⚠️ EMERGENCY if:\n" +
            "• Bone visible\n" +
            "• Severe deformity\n" +
            "• Heavy bleeding\n" +
            "• Cannot move leg",
            "✘ Do NOT move broken bone\n" +
            "✘ Do NOT straighten deformity\n" +
            "✘ Do NOT ignore blood clots\n" +
            "✘ Do NOT put weight on injury"
        ));

        BODY_DATA.put("foot_left", new BodyPartInfo(
            "Foot / Left",
            "• Ankle sprain\n" +
            "• Fractured bones\n" +
            "• Cuts/blisters\n" +
            "• Crush injury\n" +
            "• Stubbed toe",
            "1. For sprain:\n" +
            "   - Rest the foot\n" +
            "   - Apply ice wrapped\n" +
            "   - Elevate foot\n" +
            "   - Use compression bandage\n" +
            "2. For cuts:\n" +
            "   - Clean wound\n" +
            "   - Apply antiseptic\n" +
            "   - Bandage appropriately",
            "• Wear proper footwear\n" +
            "• Check feet regularly\n" +
            "• Keep feet clean/dry\n" +
            "• Trim nails carefully",
            "⚠️ Seek help if:\n" +
            "• Cannot put weight on foot\n" +
            "• Severe swelling\n" +
            "• Visible deformity\n" +
            "• Heavy bleeding",
            "✘ Do NOT ignore persistent pain\n" +
            "✘ Do NOT walk on fracture\n" +
            "✘ Do NOT pop blisters\n" +
            "✘ Do NOT ignore signs of infection"
        ));

        BODY_DATA.put("foot_right", new BodyPartInfo(
            "Foot / Right",
            "• Ankle sprain\n" +
            "• Fractured bones\n" +
            "• Cuts/blisters\n" +
            "• Crush injury\n" +
            "• Stubbed toe",
            "1. For sprain:\n" +
            "   - Rest the foot\n" +
            "   - Apply ice wrapped\n" +
            "   - Elevate foot\n" +
            "   - Use compression bandage\n" +
            "2. For cuts:\n" +
            "   - Clean wound\n" +
            "   - Apply antiseptic",
            "• Wear proper footwear\n" +
            "• Check feet regularly\n" +
            "• Keep feet clean/dry\n" +
            "• Trim nails carefully",
            "⚠️ Seek help if:\n" +
            "• Cannot put weight on foot\n" +
            "• Severe swelling\n" +
            "• Visible deformity",
            "✘ Do NOT ignore persistent pain\n" +
            "✘ Do NOT walk on fracture\n" +
            "✘ Do NOT pop blisters\n" +
            "✘ Do NOT ignore signs of infection"
        ));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_body_part_info);

        preferencesManager = new PreferencesManager(this);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        }

        textViewTitle = findViewById(R.id.textViewTitle);
        textViewInjuries = findViewById(R.id.textViewInjuries);
        textViewFirstAid = findViewById(R.id.textViewFirstAid);
        textViewPrecautions = findViewById(R.id.textViewPrecautions);
        textViewWarnings = findViewById(R.id.textViewWarnings);
        textViewDonts = findViewById(R.id.textViewDonts);

        String bodyPart = getIntent().getStringExtra("body_part");
        loadBodyPartInfo(bodyPart);

        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech.setLanguage(Locale.getDefault());
            }
        });

        findViewById(R.id.btnSpeak).setOnClickListener(v -> speakInfo());
    }

    private void loadBodyPartInfo(String bodyPart) {
        BodyPartInfo info = BODY_DATA.get(bodyPart);
        if (info == null) {
            info = BODY_DATA.get(bodyPart.replace("_left", "").replace("_right", ""));
        }
        if (info != null) {
            textViewTitle.setText(info.title);
            textViewInjuries.setText(info.injuries);
            textViewFirstAid.setText(info.firstAid);
            textViewPrecautions.setText(info.precautions);
            textViewWarnings.setText(info.warnings);
            textViewDonts.setText(info.donts);
            if (getSupportActionBar() != null) {
                getSupportActionBar().setTitle(info.title + " Safety");
            }
        }
    }

    private void speakInfo() {
        if (preferencesManager.isVoiceGuidanceEnabled()) {
            BodyPartInfo info = BODY_DATA.get(
                getIntent().getStringExtra("body_part").replace("_left", "").replace("_right", ""));
            if (info != null && textToSpeech != null) {
                String text = info.title + " safety information. " +
                    "Common injuries include: " + info.injuries.replace("\n", ". ") +
                    ". First aid steps: " + info.firstAid.replace("\n", ". ");
                textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
            }
        }
    }

    @Override
    protected void onDestroy() {
        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
        }
        super.onDestroy();
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }

    private static class BodyPartInfo {
        String title;
        String injuries;
        String firstAid;
        String precautions;
        String warnings;
        String donts;

        BodyPartInfo(String title, String injuries, String firstAid,
                     String precautions, String warnings, String donts) {
            this.title = title;
            this.injuries = injuries;
            this.firstAid = firstAid;
            this.precautions = precautions;
            this.warnings = warnings;
            this.donts = donts;
        }
    }
}
