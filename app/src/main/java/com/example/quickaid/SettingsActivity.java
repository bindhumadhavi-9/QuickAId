package com.example.quickaid;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.example.quickaid.utils.PreferencesManager;

public class SettingsActivity extends AppCompatActivity {

    private PreferencesManager preferencesManager;
    private Switch switchLargeText;
    private Switch switchHighContrast;
    private Switch switchVoiceGuidance;
    private Switch switchDarkMode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        preferencesManager = new PreferencesManager(this);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Settings");
        }

        initViews();
        loadPreferences();
    }

    private void initViews() {
        switchLargeText = findViewById(R.id.switchLargeText);
        switchHighContrast = findViewById(R.id.switchHighContrast);
        switchVoiceGuidance = findViewById(R.id.switchVoiceGuidance);
        switchDarkMode = findViewById(R.id.switchDarkMode);

        switchLargeText.setOnCheckedChangeListener(this::onLargeTextChanged);
        switchHighContrast.setOnCheckedChangeListener(this::onHighContrastChanged);
        switchVoiceGuidance.setOnCheckedChangeListener(this::onVoiceGuidanceChanged);
        switchDarkMode.setOnCheckedChangeListener(this::onDarkModeChanged);

        findViewById(R.id.btnEditSosMessage).setOnClickListener(v -> showSosMessageDialog());
        findViewById(R.id.btnRequestPermissions).setOnClickListener(v -> requestAllPermissions());
        findViewById(R.id.btnShowDisclaimer).setOnClickListener(v -> showDisclaimer());
    }

    private void loadPreferences() {
        switchLargeText.setChecked(preferencesManager.isLargeTextMode());
        switchHighContrast.setChecked(preferencesManager.isHighContrastMode());
        switchVoiceGuidance.setChecked(preferencesManager.isVoiceGuidanceEnabled());
        switchDarkMode.setChecked(preferencesManager.isDarkMode());
    }

    private void onLargeTextChanged(CompoundButton buttonView, boolean isChecked) {
        preferencesManager.setLargeTextMode(isChecked);
        applyTextSize(isChecked);
    }

    private void onHighContrastChanged(CompoundButton buttonView, boolean isChecked) {
        preferencesManager.setHighContrastMode(isChecked);
        Toast.makeText(this, "High contrast mode " + (isChecked ? "enabled" : "disabled"), Toast.LENGTH_SHORT).show();
    }

    private void onVoiceGuidanceChanged(CompoundButton buttonView, boolean isChecked) {
        preferencesManager.setVoiceGuidanceEnabled(isChecked);
        Toast.makeText(this, "Voice guidance " + (isChecked ? "enabled" : "disabled"), Toast.LENGTH_SHORT).show();
    }

    private void onDarkModeChanged(CompoundButton buttonView, boolean isChecked) {
        preferencesManager.setDarkMode(isChecked);
        Toast.makeText(this, "Dark mode " + (isChecked ? "enabled" : "disabled") + ". Restart app to apply.", Toast.LENGTH_LONG).show();
    }

    private void applyTextSize(boolean large) {
        float scale = large ? 1.25f : 1.0f;
        getResources().getConfiguration().fontScale = scale;
        // Note: Changes take effect on app restart
        Toast.makeText(this, "Text size changes will apply on app restart", Toast.LENGTH_SHORT).show();
    }

    private void showSosMessageDialog() {
        EditText input = new EditText(this);
        input.setText(preferencesManager.getSosMessageTemplate());
        input.setPadding(32, 32, 32, 32);

        new AlertDialog.Builder(this)
            .setTitle("Edit SOS Message Template")
            .setMessage("This message will be sent when you send an emergency alert")
            .setView(input)
            .setPositiveButton("Save", (dialog, which) -> {
                String newMessage = input.getText().toString().trim();
                if (!newMessage.isEmpty()) {
                    preferencesManager.setSosMessageTemplate(newMessage);
                    Toast.makeText(this, "SOS message updated", Toast.LENGTH_SHORT).show();
                }
            })
            .setNegativeButton("Cancel", null)
            .show();
    }

    private void requestAllPermissions() {
        String[] permissions = {
            Manifest.permission.CALL_PHONE,
            Manifest.permission.SEND_SMS,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        };

        boolean allGranted = true;
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                allGranted = false;
                break;
            }
        }

        if (!allGranted) {
            ActivityCompat.requestPermissions(this, permissions, 100);
        } else {
            Toast.makeText(this, "All permissions already granted", Toast.LENGTH_SHORT).show();
        }
    }

    private void showDisclaimer() {
        new AlertDialog.Builder(this)
            .setTitle("Medical Disclaimer")
            .setMessage(com.example.quickaid.utils.Constants.MEDICAL_DISCLAIMER)
            .setPositiveButton("I Understand", null)
            .show();
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}
