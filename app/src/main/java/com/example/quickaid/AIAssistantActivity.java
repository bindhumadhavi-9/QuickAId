package com.example.quickaid;

import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.utils.PreferencesManager;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class AIAssistantActivity extends AppCompatActivity {

    private EditText editTextQuery;
    private Button buttonSend;
    private ListView listViewChat;
    private TextView textViewDisclaimer;

    private List<String> chatMessages;
    private ArrayAdapter<String> chatAdapter;
    private TextToSpeech textToSpeech;
    private PreferencesManager preferencesManager;

    private static final String AI_DISCLAIMER = "I am an AI assistant providing general first-aid " +
        "information. This does not replace professional medical advice. " +
        "Always call 112 for serious emergencies.";

    private static final String[] EMERGENCY_KEYWORDS = {
        "not breathing", "unconscious", "heart attack", "severe bleeding",
        "choking", "stroke", "electric shock", "drowning"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ai_assistant);

        preferencesManager = new PreferencesManager(this);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("AI Emergency Assistant");
        }

        initViews();
        setupTextToSpeech();
        showInitialMessage();
    }

    private void initViews() {
        editTextQuery = findViewById(R.id.editTextQuery);
        buttonSend = findViewById(R.id.btnSend);
        listViewChat = findViewById(R.id.listViewChat);
        textViewDisclaimer = findViewById(R.id.textViewDisclaimer);

        chatMessages = new ArrayList<>();
        chatAdapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, chatMessages);
        listViewChat.setAdapter(chatAdapter);

        buttonSend.setOnClickListener(v -> processQuery());

        findViewById(R.id.btnNotBreathing).setOnClickListener(v ->
            processEmergencyQuery("not breathing"));
        findViewById(R.id.btnCloseBleeding).setOnClickListener(v ->
            processEmergencyQuery("severe bleeding"));
        findViewById(R.id.btnChoking).setOnClickListener(v ->
            processEmergencyQuery("choking"));
        findViewById(R.id.btnBurns).setOnClickListener(v ->
            processEmergencyQuery("burns"));
        findViewById(R.id.btnHeartAttack).setOnClickListener(v ->
            processEmergencyQuery("heart attack"));
        findViewById(R.id.btnStroke).setOnClickListener(v ->
            processEmergencyQuery("stroke"));
    }

    private void setupTextToSpeech() {
        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech.setLanguage(Locale.getDefault());
            }
        });
    }

    private void showInitialMessage() {
        addMessage("AI: Hello! I'm QuickAid's AI assistant. " +
            "I can help with first-aid guidance.\n\n" + AI_DISCLAIMER);
        if (preferencesManager.isVoiceGuidanceEnabled()) {
            speakMessage("Hello! I can help with first-aid guidance. " + AI_DISCLAIMER);
        }
    }

    private void processQuery() {
        String query = editTextQuery.getText().toString().trim();
        if (query.isEmpty()) return;

        addMessage("You: " + query);
        editTextQuery.setText("");

        String response = generateResponse(query);
        addMessage("AI: " + response);

        if (preferencesManager.isVoiceGuidanceEnabled()) {
            speakMessage(response);
        }
    }

    private void processEmergencyQuery(String emergency) {
        String response = generateEmergencyResponse(emergency);
        addMessage("You: EMERGENCY - " + emergency);
        addMessage("AI: " + response);

        if (preferencesManager.isVoiceGuidanceEnabled()) {
            speakMessage(response);
        }
    }

    private String generateResponse(String query) {
        String lowerQuery = query.toLowerCase();

        for (String keyword : EMERGENCY_KEYWORDS) {
            if (lowerQuery.contains(keyword)) {
                return generateEmergencyResponse(keyword);
            }
        }

        if (lowerQuery.contains("burn")) {
            return generateBurnResponse();
        }

        if (lowerQuery.contains("fracture") || lowerQuery.contains("broken")) {
            return generateFractureResponse();
        }

        if (lowerQuery.contains("cut") || lowerQuery.contains("wound")) {
            return generateWoundResponse();
        }

        if (lowerQuery.contains("snake")) {
            return generateSnakeBiteResponse();
        }

        if (lowerQuery.contains("heat") || lowerQuery.contains("sun")) {
            return generateHeatStrokeResponse();
        }

        if (lowerQuery.contains("seizure")) {
            return generateSeizureResponse();
        }

        if (lowerQuery.contains("help") || lowerQuery.contains("emergency")) {
            return "I'm here to help! Please describe the emergency. " +
                "You can mention: burns, cuts, fractures, choking, heart attack, stroke, " +
                "or say 'not breathing' for critical situations.";
        }

        return "I can help with first-aid guidance. Please describe the emergency or " +
            "choose from the quick options below. Common topics include: burns, " +
            "bleeding, fractures, choking, heart attack, and stroke.";
    }

    private String generateEmergencyResponse(String keyword) {
        switch (keyword) {
            case "not breathing":
                return "CRITICAL: Not breathing!\n\n" +
                    "1. Call 112 IMMEDIATELY\n" +
                    "2. Check airway - clear if blocked\n" +
                    "3. Begin CPR:\n" +
                    "   - chest compressions: 30\n" +
                    "   - rescue breaths: 2\n" +
                    "   - Repeat until help arrives\n\n" +
                    "THIS IS A LIFE-THREATENING EMERGENCY. Do not delay calling 112.";

            case "unconscious":
                return "1. Call 112 IMMEDIATELY\n" +
                    "2. Check for breathing for 10 seconds\n" +
                    "3. If breathing: place in recovery position\n" +
                    "4. If not breathing: Begin CPR\n" +
                    "5. Stay with person until help arrives";

            case "heart attack":
                return "POTENTIAL HEART ATTACK!\n\n" +
                    "1. Call 112 - say 'heart attack'\n" +
                    "2. Have person sit, stay calm\n" +
                    "3. Chew aspirin (325mg) if no allergy\n" +
                    "4. Loosen tight clothing\n" +
                    "5. Be ready to perform CPR\n" +
                    "6. Note time of symptom onset";

            case "severe bleeding":
                return "SEVERE BLEEDING!\n\n" +
                    "1. Call 112\n" +
                    "2. Apply FIRM pressure with clean cloth\n" +
                    "3. Do NOT remove first bandage - add more\n" +
                    "4. Elevate if possible\n" +
                    "5. Keep pressure until help arrives";

            case "choking":
                return "1. If person can cough, encourage coughing\n" +
                    "2. If cannot cough/speak/breathe:\n" +
                    "   - Give 5 back blows between shoulders\n" +
                    "   - Give 5 abdominal thrusts (Heimlich)\n" +
                    "3. Alternate until obstruction clears\n" +
                    "4. Call 112 if not clearing quickly";

            case "stroke":
                return "POTENTIAL STROKE - Act FAST!\n\n" +
                    "Face: Ask them to smile - does one side droop?\n" +
                    "Arms: Can they raise both arms?\n" +
                    "Speech: Is speech slurred?\n" +
                    "Time: Call 112 NOW if ANY symptom\n\n" +
                    "Note exact time symptoms started. " +
                    "Treatment window is 3-4.5 hours.";

            case "electric shock":
                return "1. DO NOT touch person if power still on\n" +
                    "2. Turn off power at source\n" +
                    "or use dry wood to separate from source\n" +
                    "3. Call 112 - electrical injuries always serious\n" +
                    "4. Begin CPR if not breathing\n" +
                    "5. Monitor breathing continuously";

            case "drowning":
                return "1. Call for help immediately\n" +
                    "2. Reach/throw - Do not enter unless trained\n" +
                    "3. Rescue and check breathing immediately\n" +
                    "4. If not breathing - begin CPR\n" +
                    "5. If breathing - recovery position, keep warm\n" +
                    "6. ALL drowning victims need medical attention";

            default:
                return "Please describe the emergency more specifically.";
        }
    }

    private String generateBurnResponse() {
        return "BURN TREATMENT:\n\n" +
            "1. Run cool water for 10-20 minutes\n" +
            "2. Remove jewelry near burn\n" +
            "3. Cover loosely with clean cloth\n" +
            "4. Do NOT use ice, butter, or oil\n" +
            "5. Do NOT break blisters\n\n" +
            "Call 112 if: large burn area, electrical/chemical, face/hands/genitals.";
    }

    private String generateFractureResponse() {
        return "FRACTURE TREATMENT:\n\n" +
            "1. Do NOT move the person\n" +
            "2. Immobilize with makeshift splint\n" +
            "3. Apply ice wrapped in cloth\n" +
            "4. Do NOT try to straighten bone\n" +
            "5. Seek medical attention\n\n" +
            "Call 112 if: bone visible, spine suspected, severe deformity.";
    }

    private String generateWoundResponse() {
        return "CUT/WOUND TREATMENT:\n\n" +
            "1. Apply direct pressure with clean cloth\n" +
            "2. If minor, clean with water and antiseptic\n" +
            "3. Apply bandage\n" +
            "4. Elevate if possible\n" +
            "5. Watch for infection signs\n\n" +
            "Seek help if: severe bleeding, deep wound, embedded object, tetanus concern.";
    }

    private String generateSnakeBiteResponse() {
        return "SNAKE BITE:\n\n" +
            "1. Move away from snake\n" +
            "2. Keep person calm\n" +
            "3. Call 112 IMMEDIATELY\n" +
            "4. Immobilize bitten limb - keep BELOW heart\n" +
            "5. Note time and snake appearance\n\n" +
            "Do NOT: cut, suck, tourniquet, use ice.";
    }

    private String generateHeatStrokeResponse() {
        return "HEAT STROKE:\n\n" +
            "1. Move to cool area immediately\n" +
            "2. Call 112\n" +
            "3. Remove excess clothing\n" +
            "4. Cool rapidly - wet skin, fan, ice packs to neck/armpits\n" +
            "5. If conscious, sip cool water\n" +
            "6. Monitor temperature\n\n" +
            "Signs: temp above 40C (104F), confusion, hot dry skin.";
    }

    private String generateSeizureResponse() {
        return "SEIZURE FIRST AID:\n\n" +
            "1. Stay calm - note time\n" +
            "2. Clear area of hazards\n" +
            "3. Cushion head\n" +
            "4. Turn to side after seizure\n" +
            "5. Stay until fully alert\n\n" +
            "Do NOT: restrain, put anything in mouth, hold tongue.\n" +
            "Call 112 if: first seizure, longer than 5 min, injury, pregnant.";
    }

    private void addMessage(String message) {
        chatMessages.add(message);
        chatAdapter.notifyDataSetChanged();
        listViewChat.setSelection(chatMessages.size() - 1);
    }

    private void speakMessage(String message) {
        if (textToSpeech != null) {
            String textOnly = message.replaceAll("[^a-zA-Z0-9 .,]", " ");
            textToSpeech.speak(textOnly, TextToSpeech.QUEUE_FLUSH, null, null);
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
}
