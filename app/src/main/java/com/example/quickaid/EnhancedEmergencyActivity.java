package com.example.quickaid;

import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.utils.PreferencesManager;

import java.util.Locale;

public class EnhancedEmergencyActivity extends AppCompatActivity {

    private TextView textViewTitle;
    private TextView textViewSeverity;
    private TextView textViewDescription;
    private TextView textViewSymptoms;
    private TextView textViewSteps;
    private TextView textViewDos;
    private TextView textViewDonts;
    private TextView textViewWhenToCall;
    private ScrollView scrollView;
    private Button btnCallEmergency;
    private Button btnVoiceGuide;
    private View severityIndicator;

    private TextToSpeech textToSpeech;
    private PreferencesManager preferencesManager;

    private String emergencyType;
    private EmergencyWorkflow currentWorkflow;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enhanced_emergency);

        preferencesManager = new PreferencesManager(this);

        emergencyType = getIntent().getStringExtra("emergency_type");
        if (emergencyType == null) {
            emergencyType = "road_accident";
        }

        initViews();
        loadEmergencyWorkflow();
        setupTextToSpeech();
    }

    private void initViews() {
        textViewTitle = findViewById(R.id.textViewTitle);
        textViewSeverity = findViewById(R.id.textViewSeverity);
        textViewDescription = findViewById(R.id.textViewDescription);
        textViewSymptoms = findViewById(R.id.textViewSymptoms);
        textViewSteps = findViewById(R.id.textViewSteps);
        textViewDos = findViewById(R.id.textViewDos);
        textViewDonts = findViewById(R.id.textViewDonts);
        textViewWhenToCall = findViewById(R.id.textViewWhenToCall);
        scrollView = findViewById(R.id.scrollView);
        btnCallEmergency = findViewById(R.id.btnCallEmergency);
        severityIndicator = findViewById(R.id.severityIndicator);
        btnVoiceGuide = findViewById(R.id.btnVoiceGuide);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        }

        btnCallEmergency.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_DIAL);
            intent.setData(android.net.Uri.parse("tel:112"));
            startActivity(intent);
        });

        btnVoiceGuide.setOnClickListener(v -> speakInstructions());
    }

    private void loadEmergencyWorkflow() {
        currentWorkflow = EmergencyWorkflowData.getWorkflow(emergencyType);
        if (currentWorkflow != null) {
            displayWorkflow(currentWorkflow);
        }
    }

    private void displayWorkflow(EmergencyWorkflow workflow) {
        textViewTitle.setText(workflow.getTitle());

        // Set severity
        String severityText = getSeverityText(workflow.getSeverityLevel());
        textViewSeverity.setText("Severity: " + severityText);
        setSeverityColor(workflow.getSeverityLevel());

        textViewDescription.setText(workflow.getDescription());

        StringBuilder symptomsBuilder = new StringBuilder();
        for (String symptom : workflow.getSymptoms()) {
            symptomsBuilder.append("• ").append(symptom).append("\n");
        }
        textViewSymptoms.setText(symptomsBuilder.toString());

        StringBuilder stepsBuilder = new StringBuilder();
        int step = 1;
        for (String stepText : workflow.getSteps()) {
            stepsBuilder.append(step++).append(". ").append(stepText).append("\n\n");
        }
        textViewSteps.setText(stepsBuilder.toString());

        StringBuilder dosBuilder = new StringBuilder();
        for (String doItem : workflow.getDos()) {
            dosBuilder.append("✔ ").append(doItem).append("\n");
        }
        textViewDos.setText(dosBuilder.toString());

        StringBuilder dontsBuilder = new StringBuilder();
        for (String dontItem : workflow.getDonts()) {
            dontsBuilder.append("✘ ").append(dontItem).append("\n");
        }
        textViewDonts.setText(dontsBuilder.toString());

        textViewWhenToCall.setText(workflow.getWhenToCallEmergency());

        if (getSupportActionBar() != null) {
            getSupportActionBar().setTitle(workflow.getTitle());
        }
    }

    private String getSeverityText(int level) {
        switch (level) {
            case 1: return "LOW - Monitor";
            case 2: return "MEDIUM - Seek Medical Attention";
            case 3: return "HIGH - Urgent Medical Care Needed";
            case 4: return "CRITICAL - Call 112 Immediately";
            default: return "UNKNOWN";
        }
    }

    private void setSeverityColor(int level) {
        int color;
        switch (level) {
            case 1: color = getResources().getColor(R.color.severity_low); break;
            case 2: color = getResources().getColor(R.color.severity_medium); break;
            case 3: color = getResources().getColor(R.color.severity_high); break;
            case 4: color = getResources().getColor(R.color.severity_critical); break;
            default: color = getResources().getColor(R.color.text_secondary);
        }
        severityIndicator.setBackgroundColor(color);
    }

    private void setupTextToSpeech() {
        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech.setLanguage(Locale.getDefault());
            }
        });
    }

    private void speakInstructions() {
        if (preferencesManager.isVoiceGuidanceEnabled() && currentWorkflow != null && textToSpeech != null) {
            StringBuilder speechText = new StringBuilder();
            speechText.append(currentWorkflow.getTitle()).append(". ");

            int step = 1;
            for (String stepText : currentWorkflow.getSteps()) {
                speechText.append("Step ").append(step++).append(": ").append(stepText).append(". ");
            }

            textToSpeech.speak(speechText.toString(), TextToSpeech.QUEUE_FLUSH, null, null);
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
