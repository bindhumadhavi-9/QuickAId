package com.example.quickaid.utils;

public class Constants {
    // Emergency Numbers - India
    public static final String EMERGENCY_NUMBER = "112";
    public static final String AMBULANCE_NUMBER = "108";
    public static final String POLICE_NUMBER = "100";
    public static final String FIRE_NUMBER = "101";
    public static final String WOMEN_HELPLINE = "1091";
    public static final String CHILD_HELPLINE = "1098";

    // Relationships for emergency contacts
    public static final String[] RELATIONSHIPS = {
        "Father", "Mother", "Brother", "Sister", "Guardian",
        "Friend", "Doctor", "Spouse", "Relative", "Other"
    };

    // First Aid Kit Default Items
    public static final String[] DEFAULT_FIRST_AID_ITEMS = {
        "Bandages", "Cotton", "Antiseptic Liquid", "Burn Cream",
        "Pain Relief Spray", "Thermometer", "Gloves", "Medical Tape",
        "Scissors", "Face Masks", "Hand Sanitizer", "ORS Packets",
        "Paracetamol Tablets", "Cough Tablets", "Pain Relief Tablets",
        "Antiseptic Ointment", "Sterile Gauze", "Adhesive Bandages",
        "Tweezers", "Safety Pins", "Flashlight", "Emergency Blanket"
    };

    // Quiz Categories
    public static final String[] QUIZ_CATEGORIES = {
        "burns", "choking", "bleeding", "fractures",
        "electric_shock", "heart_attack", "cpr", "stroke",
        "drowning", "snake_bite", "general"
    };

    // Emergency Types
    public static final String[] EMERGENCY_TYPES = {
        "Road Accident", "Burns", "Electric Shock", "Fractures",
        "Choking", "Drowning", "Snake Bite", "Dog Bite",
        "Heart Attack", "Stroke", "Heat Stroke", "Food Poisoning",
        "Seizures", "Unconscious Person", "Heavy Bleeding"
    };

    // Decision Tree Questions
    public static final String[] DECISION_QUESTIONS = {
        "Is the victim conscious?",
        "Is the victim breathing?",
        "Is there severe bleeding?",
        "Is there a suspected fracture?",
        "Is the victim responsive to voice?"
    };

    // Severity Levels
    public static final int SEVERITY_LOW = 1;
    public static final int SEVERITY_MEDIUM = 2;
    public static final int SEVERITY_HIGH = 3;
    public static final int SEVERITY_CRITICAL = 4;

    // Shared Preferences
    public static final String PREF_NAME = "QuickAidPrefs";
    public static final String PREF_LARGE_TEXT = "large_text_mode";
    public static final String PREF_HIGH_CONTRAST = "high_contrast_mode";
    public static final String PREF_VOICE_GUIDANCE = "voice_guidance";
    public static final String PREF_DARK_MODE = "dark_mode";

    // Request Codes
    public static final int CALL_PERMISSION_REQUEST = 100;
    public static final int LOCATION_PERMISSION_REQUEST = 101;
    public static final int SMS_PERMISSION_REQUEST = 102;

    // Disclaimer
    public static final String MEDICAL_DISCLAIMER = "IMPORTANT: QuickAid provides general first-aid " +
        "information for educational purposes. This app does not replace professional medical advice, " +
        "diagnosis, or treatment. Always seek the advice of a qualified healthcare provider for any " +
        "medical emergency. If you are experiencing a medical emergency, call emergency services " +
        "immediately.";
}
