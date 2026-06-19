package com.example.quickaid;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.example.quickaid.database.AppDatabase;
import com.example.quickaid.models.EmergencyContact;
import com.example.quickaid.utils.Constants;
import com.example.quickaid.utils.PreferencesManager;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private static final int CALL_PERMISSION_REQUEST = 100;
    private static final int SMS_PERMISSION_REQUEST = 101;

    private Button btnEmergency, btnBodyGuide, btnTips, btnContacts, btnNearby,
            btnKit, btnQuiz, btnAI, btnPreparedness, btnDecisionTree, btnSettings;
    private LinearLayout sosCard, hotlineAmbulance, hotlinePolice, hotlineFire;

    private AppDatabase database;
    private PreferencesManager preferencesManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        preferencesManager = new PreferencesManager(this);
        database = AppDatabase.getDatabase(this);

        initViews();
        setupClickListeners();

        if (preferencesManager.isFirstLaunch()) {
            showDisclaimerDialog();
            preferencesManager.setFirstLaunchComplete();
        }
    }

    private void initViews() {
        sosCard = findViewById(R.id.sosCard);
        btnEmergency = findViewById(R.id.btnEmergency);
        btnBodyGuide = findViewById(R.id.btnBodyGuide);
        btnContacts = findViewById(R.id.btnContacts);
        btnNearby = findViewById(R.id.btnNearby);
        btnTips = findViewById(R.id.btnTips);
        btnKit = findViewById(R.id.btnKit);
        btnQuiz = findViewById(R.id.btnQuiz);
        btnAI = findViewById(R.id.btnAI);
        btnPreparedness = findViewById(R.id.btnPreparedness);
        btnDecisionTree = findViewById(R.id.btnDecisionTree);
        btnSettings = findViewById(R.id.btnSettings);

        hotlineAmbulance = findViewById(R.id.hotlineAmbulance);
        hotlinePolice = findViewById(R.id.hotlinePolice);
        hotlineFire = findViewById(R.id.hotlineFire);
    }

    private void setupClickListeners() {
        sosCard.setOnClickListener(v -> showSOSConfirmationDialog());

        btnEmergency.setOnClickListener(v -> navigateTo(EmergencyActivity.class));
        btnBodyGuide.setOnClickListener(v -> navigateTo(BodyGuideActivity.class));
        btnContacts.setOnClickListener(v -> navigateTo(ContactsManagerActivity.class));
        btnNearby.setOnClickListener(v -> navigateTo(NearbyServicesActivity.class));
        btnTips.setOnClickListener(v -> navigateTo(TipsActivity.class));
        btnKit.setOnClickListener(v -> navigateTo(FirstAidKitActivity.class));
        btnQuiz.setOnClickListener(v -> navigateTo(QuizActivity.class));
        btnAI.setOnClickListener(v -> navigateTo(AIAssistantActivity.class));
        btnPreparedness.setOnClickListener(v -> navigateTo(PreparednessActivity.class));
        btnDecisionTree.setOnClickListener(v -> navigateTo(DecisionTreeActivity.class));
        btnSettings.setOnClickListener(v -> navigateTo(SettingsActivity.class));

        hotlineAmbulance.setOnClickListener(v -> makeEmergencyCall(Constants.AMBULANCE_NUMBER));
        hotlinePolice.setOnClickListener(v -> makeEmergencyCall(Constants.POLICE_NUMBER));
        hotlineFire.setOnClickListener(v -> makeEmergencyCall(Constants.FIRE_NUMBER));
    }

    private void showSOSConfirmationDialog() {
        new AlertDialog.Builder(this)
            .setTitle("EMERGENCY SOS")
            .setMessage("This will immediately call emergency services (112).\n\nAre you in an emergency situation?")
            .setPositiveButton("CALL NOW", (dialog, which) -> makeEmergencyCall(Constants.EMERGENCY_NUMBER))
            .setNegativeButton("Cancel", null)
            .setCancelable(true)
            .show();
    }

    private void makeEmergencyCall(String phoneNumber) {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.CALL_PHONE}, CALL_PERMISSION_REQUEST);
        } else {
            Intent callIntent = new Intent(Intent.ACTION_CALL);
            callIntent.setData(Uri.parse("tel:" + phoneNumber));
            startActivity(callIntent);
        }
    }

    private void sendEmergencySMS(String phoneNumber, String message) {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.SEND_SMS}, SMS_PERMISSION_REQUEST);
        } else {
            try {
                SmsManager smsManager = SmsManager.getDefault();
                smsManager.sendTextMessage(phoneNumber, null, message, null, null);
                Toast.makeText(this, "Emergency SMS sent", Toast.LENGTH_SHORT).show();
            } catch (Exception e) {
                Toast.makeText(this, "Failed to send SMS", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void showDisclaimerDialog() {
        new AlertDialog.Builder(this)
            .setTitle("Important Medical Disclaimer")
            .setMessage(Constants.MEDICAL_DISCLAIMER)
            .setPositiveButton("I Understand", null)
            .setCancelable(false)
            .show();
    }

    private void navigateTo(Class<?> activityClass) {
        startActivity(new Intent(this, activityClass));
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                            @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CALL_PERMISSION_REQUEST) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                makeEmergencyCall(Constants.EMERGENCY_NUMBER);
            } else {
                Toast.makeText(this, "Call permission is required for emergency calls",
                    Toast.LENGTH_LONG).show();
            }
        } else if (requestCode == SMS_PERMISSION_REQUEST) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Retry sending SMS
                Toast.makeText(this, "SMS permission granted. Try again.", Toast.LENGTH_SHORT).show();
            }
        }
    }
}
