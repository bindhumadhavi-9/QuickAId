package com.example.quickaid.utils;

import android.content.Context;
import android.content.SharedPreferences;

public class PreferencesManager {
    private static final String PREF_NAME = "QuickAidPrefs";

    // Keys
    private static final String KEY_LARGE_TEXT = "large_text_mode";
    private static final String KEY_HIGH_CONTRAST = "high_contrast_mode";
    private static final String KEY_VOICE_GUIDANCE = "voice_guidance_enabled";
    private static final String KEY_DARK_MODE = "dark_mode";
    private static final String KEY_FIRST_LAUNCH = "first_launch";
    private static final String KEY_SOS_MESSAGE = "sos_message_template";
    private static final String KEY_LOCATION_HELP_SHOWN = "location_help_shown";

    private final SharedPreferences preferences;

    public PreferencesManager(Context context) {
        preferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    // Large Text Mode
    public boolean isLargeTextMode() {
        return preferences.getBoolean(KEY_LARGE_TEXT, false);
    }

    public void setLargeTextMode(boolean enabled) {
        preferences.edit().putBoolean(KEY_LARGE_TEXT, enabled).apply();
    }

    // High Contrast Mode
    public boolean isHighContrastMode() {
        return preferences.getBoolean(KEY_HIGH_CONTRAST, false);
    }

    public void setHighContrastMode(boolean enabled) {
        preferences.edit().putBoolean(KEY_HIGH_CONTRAST, enabled).apply();
    }

    // Voice Guidance
    public boolean isVoiceGuidanceEnabled() {
        return preferences.getBoolean(KEY_VOICE_GUIDANCE, false);
    }

    public void setVoiceGuidanceEnabled(boolean enabled) {
        preferences.edit().putBoolean(KEY_VOICE_GUIDANCE, enabled).apply();
    }

    // Dark Mode
    public boolean isDarkMode() {
        return preferences.getBoolean(KEY_DARK_MODE, true);
    }

    public void setDarkMode(boolean enabled) {
        preferences.edit().putBoolean(KEY_DARK_MODE, enabled).apply();
    }

    // First Launch
    public boolean isFirstLaunch() {
        return preferences.getBoolean(KEY_FIRST_LAUNCH, true);
    }

    public void setFirstLaunchComplete() {
        preferences.edit().putBoolean(KEY_FIRST_LAUNCH, false).apply();
    }

    // SOS Message Template
    public String getSosMessageTemplate() {
        return preferences.getString(KEY_SOS_MESSAGE,
            "EMERGENCY! I need help immediately. This is an automated emergency alert from QuickAid.");
    }

    public void setSosMessageTemplate(String message) {
        preferences.edit().putString(KEY_SOS_MESSAGE, message).apply();
    }

    // Location Help Shown
    public boolean isLocationHelpShown() {
        return preferences.getBoolean(KEY_LOCATION_HELP_SHOWN, false);
    }

    public void setLocationHelpShown(boolean shown) {
        preferences.edit().putBoolean(KEY_LOCATION_HELP_SHOWN, shown).apply();
    }

    // Clear all preferences (for testing/reset)
    public void clearAll() {
        preferences.edit().clear().apply();
    }
}
