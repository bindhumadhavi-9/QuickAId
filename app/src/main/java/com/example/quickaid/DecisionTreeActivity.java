package com.example.quickaid;

import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.utils.PreferencesManager;

import java.util.Locale;

public class DecisionTreeActivity extends AppCompatActivity {

    private TextView textViewQuestion;
    private RadioGroup radioGroupOptions;
    private RadioButton radioButtonYes;
    private RadioButton radioButtonNo;
    private Button buttonNext;
    private TextView textViewResult;
    private TextView textViewStep;
    private TextView textViewWarning;

    private int currentStep = 0;
    private boolean[] answers = new boolean[5];
    private PreferencesManager preferencesManager;
    private TextToSpeech textToSpeech;

    private final String[] questions = {
        "Is the victim conscious?",
        "Is the victim breathing?",
        "Is there severe bleeding?",
        "Is there a suspected fracture or spinal injury?",
        "Is the victim responsive to your voice?"
    };

    private String currentResult = "";
    private boolean isComplete = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_decision_tree);

        preferencesManager = new PreferencesManager(this);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Emergency Guide");
        }

        initView();
        setupTextToSpeech();
        showQuestion(0);
    }

    private void initView() {
        textViewQuestion = findViewById(R.id.textViewQuestion);
        radioGroupOptions = findViewById(R.id.radioGroupOptions);
        radioButtonYes = findViewById(R.id.radioButtonYes);
        radioButtonNo = findViewById(R.id.radioButtonNo);
        buttonNext = findViewById(R.id.buttonNext);
        textViewResult = findViewById(R.id.textViewResult);
        textViewStep = findViewById(R.id.textViewStep);
        textViewWarning = findViewById(R.id.textViewWarning);

        buttonNext.setOnClickListener(v -> processAnswer());
    }

    private void setupTextToSpeech() {
        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech.setLanguage(Locale.getDefault());
            }
        });
    }

    private void showQuestion(int step) {
        if (step >= questions.length) {
            showFinalResult();
            return;
        }

        currentStep = step;
        textViewStep.setText("Step " + (step + 1) + " of " + questions.length);
        textViewQuestion.setText(questions[step]);
        radioGroupOptions.clearCheck();
        textViewResult.setVisibility(View.GONE);
        textViewWarning.setVisibility(View.GONE);
        buttonNext.setText(step == questions.length - 1 ? "Get Guidance" : "Next");
        isComplete = false;

        if (preferencesManager.isVoiceGuidanceEnabled()) {
            speakQuestion(questions[step]);
        }
    }

    private void processAnswer() {
        int selectedId = radioGroupOptions.getCheckedRadioButtonId();
        if (selectedId == -1) {
            textViewResult.setVisibility(View.VISIBLE);
            textViewResult.setText("Please select Yes or No");
            textViewResult.setTextColor(getResources().getColor(R.color.warning_orange));
            return;
        }

        answers[currentStep] = selectedId == R.id.radioButtonYes;

        if (showImmediateGuidanceIfNeeded()) {
            return;
        }

        showQuestion(currentStep + 1);
    }

    private boolean showImmediateGuidanceIfNeeded() {
        // Immediate life-threatening conditions
        if (currentStep == 0 && !answers[0]) {
            // Not conscious
            showResult(
                "UNCONSCIOUS PERSON",
                "The person is unconscious. This is a MEDICAL EMERGENCY.\n\n" +
                "IMMEDIATE ACTIONS:\n" +
                "1. Call 112 IMMEDIATELY\n" +
                "2. Check if breathing\n" +
                "3. If not breathing, start CPR\n" +
                "4. If breathing, place in recovery position\n" +
                "5. Stay with person until help arrives",
                4
            );
            return true;
        }

        if (currentStep == 1 && !answers[1]) {
            // Not breathing
            showResult(
                "NOT BREATHING - CARDIAC ARREST",
                "The person is not breathing. This is CRITICAL.\n\n" +
                "IMMEDIATE ACTIONS:\n" +
                "1. Call 112 IMMEDIATELY\n" +
                "2. Begin CPR immediately:\n" +
                "   - 30 chest compressions\n" +
                "   - 2 rescue breaths\n" +
                "   - Continue until help arrives\n" +
                "3. Ask someone to find an AED",
                4
            );
            return true;
        }

        if (currentStep == 2 && answers[2]) {
            // Severe bleeding
            showResult(
                "SEVERE BLEEDING",
                "Heavy bleeding requires immediate action.\n\n" +
                "IMMEDIATE ACTIONS:\n" +
                "1. Call 112\n" +
                "2. Apply FIRM direct pressure with clean cloth\n" +
                "3. Do NOT remove first bandage - add more\n" +
                "4. Elevate if possible\n" +
                "5. Press firmly and continuously\n\n" +
                "Continue to complete full assessment.",
                4
            );
            return false;
        }

        return false;
    }

    private void showFinalResult() {
        isComplete = true;
        String guidance = determineGuidance();
        int severity = calculateSeverity();

        String title;
        if (severity >= 4) {
            title = "CRITICAL - Call 112 Immediately";
        } else if (severity >= 3) {
            title = "URGENT - Seek Medical Attention";
        } else if (severity >= 2) {
            title = "MODERATE - Monitor Closely";
        } else {
            title = "STABLE - Continue Monitoring";
        }

        showResult(title, guidance, severity);
    }

    private String determineGuidance() {
        StringBuilder guidance = new StringBuilder();
        guidance.append("Based on your responses:\n\n");

        boolean conscious = answers[0];
        boolean breathing = answers[1];
        boolean severeBleeding = answers[2];
        boolean fracture = answers[3];
        boolean responsive = answers[4];

        if (!conscious) {
            guidance.append("• Person is unconscious - CALL 112\n");
        }

        if (!breathing) {
            guidance.append("• Person not breathing - Begin CPR\n");
        }

        if (severeBleeding) {
            guidance.append("• Control bleeding with direct pressure\n");
        }

        if (fracture) {
            guidance.append("• Immobilize suspected fracture\n");
            guidance.append("• Do NOT move person unnecessarily\n");
        }

        if (!responsive && conscious) {
            guidance.append("• Person may have head injury or stroke\n");
            guidance.append("• Check FAST signs for stroke\n");
        }

        if (breathing && conscious && responsive && !severeBleeding) {
            guidance.append("• Monitor vital signs\n");
            guidance.append("• Keep person comfortable and calm\n");
            guidance.append("• Watch for any changes in condition\n");
        }

        guidance.append("\nGENERAL STEPS:\n");
        guidance.append("1. Stay calm and reassuring\n");
        guidance.append("2. Keep person warm\n");
        guidance.append("3. Do not give food or water if serious injury\n");
        guidance.append("4. Note symptoms for emergency responders\n");
        guidance.append("5. Stay with person until help arrives\n");

        return guidance.toString();
    }

    private int calculateSeverity() {
        int severity = 1;

        if (!answers[1]) severity = 4; // Not breathing
        if (!answers[0]) severity = 4; // Not conscious
        if (answers[2]) severity = Math.max(severity, 3); // Severe bleeding
        if (answers[3]) severity = Math.max(severity, 3); // Fracture
        if (!answers[4] && answers[0]) severity = Math.max(severity, 3); // Not responsive but conscious

        return severity;
    }

    private void showResult(String title, String result, int severity) {
        textViewStep.setText("Assessment Complete");
        textViewQuestion.setText(title);
        radioGroupOptions.setVisibility(View.GONE);
        buttonNext.setVisibility(View.GONE);
        textViewResult.setVisibility(View.VISIBLE);
        textViewResult.setText(result);

        int color;
        switch (severity) {
            case 4: color = getResources().getColor(R.color.severity_critical); break;
            case 3: color = getResources().getColor(R.color.severity_high); break;
            case 2: color = getResources().getColor(R.color.severity_medium); break;
            default: color = getResources().getColor(R.color.severity_low); break;
        }
        textViewQuestion.setTextColor(color);

        if (severity >= 4) {
            textViewWarning.setVisibility(View.VISIBLE);
            textViewWarning.setText("⚠️ CALL 112 NOW - This is a medical emergency");
        }

        if (preferencesManager.isVoiceGuidanceEnabled()) {
            speakResult(title + ". " + result);
        }

        findViewById(R.id.btnRestart).setVisibility(View.VISIBLE);
        findViewById(R.id.btnRestart).setOnClickListener(v -> restartAssessment());
    }

    private void speakQuestion(String question) {
        if (textToSpeech != null) {
            textToSpeech.speak(question, TextToSpeech.QUEUE_FLUSH, null, null);
        }
    }

    private void speakResult(String result) {
        if (textToSpeech != null) {
            textToSpeech.speak(result, TextToSpeech.QUEUE_FLUSH, null, null);
        }
    }

    private void restartAssessment() {
        currentStep = 0;
        answers = new boolean[5];
        radioGroupOptions.setVisibility(View.VISIBLE);
        buttonNext.setVisibility(View.VISIBLE);
        findViewById(R.id.btnRestart).setVisibility(View.GONE);
        textViewQuestion.setTextColor(getResources().getColor(R.color.white));
        showQuestion(0);
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
