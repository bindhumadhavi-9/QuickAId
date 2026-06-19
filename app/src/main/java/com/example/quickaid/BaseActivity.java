package com.example.quickaid;

import android.content.Intent;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.utils.PreferencesManager;

import java.util.HashMap;
import java.util.Locale;

public abstract class BaseActivity extends AppCompatActivity implements TextToSpeech.OnInitListener {

    protected TextToSpeech textToSpeech;
    protected boolean ttsInitialized = false;
    protected PreferencesManager preferencesManager;

    @Override
    protected void onStart() {
        super.onStart();
        if (textToSpeech == null) {
            textToSpeech = new TextToSpeech(this, this);
        }
        preferencesManager = new PreferencesManager(this);
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
            textToSpeech = null;
            ttsInitialized = false;
        }
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            int result = textToSpeech.setLanguage(Locale.getDefault());
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                result = textToSpeech.setLanguage(Locale.US);
            }
            ttsInitialized = (result != TextToSpeech.LANG_MISSING_DATA && result != TextToSpeech.LANG_NOT_SUPPORTED);

            textToSpeech.setOnUtteranceProgressListener(new UtteranceProgressListener() {
                @Override
                public void onStart(String utteranceId) {}

                @Override
                public void onDone(String utteranceId) {}

                @Override
                public void onError(String utteranceId) {}
            });
        } else {
            ttsInitialized = false;
        }
    }

    protected void speakText(String text) {
        if (preferencesManager != null && preferencesManager.isVoiceGuidanceEnabled() && ttsInitialized && textToSpeech != null) {
            HashMap<String, String> params = new HashMap<>();
            params.put(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, String.valueOf(System.currentTimeMillis()));
            textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, params);
        }
    }

    protected void speakTextQueue(String text) {
        if (preferencesManager != null && preferencesManager.isVoiceGuidanceEnabled() && ttsInitialized && textToSpeech != null) {
            HashMap<String, String> params = new HashMap<>();
            params.put(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, String.valueOf(System.currentTimeMillis()));
            textToSpeech.speak(text, TextToSpeech.QUEUE_ADD, params);
        }
    }

    protected void stopSpeaking() {
        if (textToSpeech != null) {
            textToSpeech.stop();
        }
    }

    protected void showToast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }

    protected void showToastLong(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    protected void navigateTo(Class<?> activityClass) {
        startActivity(new Intent(this, activityClass));
    }
}
