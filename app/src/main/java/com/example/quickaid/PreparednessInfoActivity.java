package com.example.quickaid;

import android.os.Bundle;
import android.widget.TextView;
import android.speech.tts.TextToSpeech;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class PreparednessInfoActivity extends AppCompatActivity {

    private TextToSpeech textToSpeech;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preparedness_info);

        String disasterType = getIntent().getStringExtra("disaster_type");
        if (disasterType == null) disasterType = "general";

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        }

        loadDisasterInfo(disasterType);
        setupTTS(disasterType);

        findViewById(R.id.btnVoiceRead).setOnClickListener(v -> readAloud(disasterType));
    }

    private void setupTTS(String type) {
        textToSpeech = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech.setLanguage(Locale.getDefault());
            }
        });
    }

    private void loadDisasterInfo(String type) {
        TextView textViewTitle = findViewById(R.id.textViewTitle);
        TextView textViewBefore = findViewById(R.id.textViewBefore);
        TextView textViewDuring = findViewById(R.id.textViewDurng);
        TextView textViewAfter = findViewById(R.id.textViewAfter);
        TextView textViewTips = findViewById(R.id.textViewTips);
        TextView textViewWarning = findViewById(R.id.textViewWarning);

        DisasterInfo info = getDisasterInfo(type);

        textViewTitle.setText(info.title);
        textViewBefore.setText(info.before);
        textViewDuring.setText(info.during);
        textViewAfter.setText(info.after);
        textViewTips.setText(info.tips);
        textViewWarning.setText(info.warning);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setTitle(info.title);
        }
    }

    private DisasterInfo getDisasterInfo(String type) {
        switch (type) {
            case "earthquake":
                return new DisasterInfo(
                    "Earthquake Safety",
                    "BEFORE:\n" +
                    "• Identify safe spots (under sturdy furniture, against interior walls)\n" +
                    "• Practice Drop, Cover, Hold On drills\n" +
                    "• Secure heavy furniture and appliances\n" +
                    "• Prepare emergency kit\n" +
                    "• Know evacuation routes\n" +
                    "• Keep important documents accessible",

                    "DURING:\n" +
                    "• DROP to hands and knees\n" +
                    "• Take COVER under sturdy furniture or against interior wall\n" +
                    "• HOLD ON until shaking stops\n" +
                    "• Stay away from windows, heavy objects\n" +
                    "• If outdoors, move to open area away from buildings\n" +
                    "• If driving, pull over safely and stay inside\n" +
                    "• Do NOT use elevator\n" +
                    "• Do NOT run outside during shaking",

                    "AFTER:\n" +
                    "• Check yourself and others for injuries\n" +
                    "• Be prepared for aftershocks\n" +
                    "• Check for gas leaks, fire hazards\n" +
                    "• Stay away from damaged buildings\n" +
                    "• Use text messages to communicate\n" +
                    "• Follow instructions from authorities",

                    "TIPS:\n" +
                    "• Create a family communication plan\n" +
                    "• Set a meeting point\n" +
                    "• Keep emergency numbers accessible\n" +
                    "• Store water and non-perishable food\n" +
                    "• Learn first aid and CPR",

                    "If you smell gas, leave immediately. Do NOT use matches or electrical switches."
                );

            case "flood":
                return new DisasterInfo(
                    "Flood Safety",
                    "BEFORE:\n" +
                    "• Know your flood risk level\n" +
                    "• Elevate electrical appliances\n" +
                    "• Store important documents in waterproof containers\n" +
                    "• Have evacuation plan ready\n" +
                    "• Prepare emergency kit with waterproof items\n" +
                    "• Never build in flood-prone areas\n" +
                    "• Install check valves in plumbing",

                    "DURING:\n" +
                    "• Move to higher ground immediately\n" +
                    "• Do NOT walk through moving water - 6 inches can knock you down\n" +
                    "• Do NOT drive through flooded roads - Turn Around, Don't Drown\n" +
                    "• Stay off bridges over fast-moving water\n" +
                    "• If trapped in building, go to highest level\n" +
                    "• Listen to emergency broadcasts\n" +
                    "• Disconnect electrical appliances if safe",

                    "AFTER:\n" +
                    "• Avoid flood water - may be contaminated\n" +
                    "• Do NOT enter damaged buildings until declared safe\n" +
                    "• Clean and disinfect everything wet\n" +
                    "• Take photos of damage for insurance\n" +
                    "• Watch for snakes and other animals\n" +
                    "• Only use tap water if declared safe\n" +
                    "• Dispose of food that touched flood water",

                    "TIPS:\n" +
                    "• Keep important numbers in your phone\n" +
                    "• Have a battery radio\n" +
                    "• Keep vehicle fueled\n" +
                    "• Memorize nearby high ground\n" +
                    "• Teach family flood safety",

                    "Never drive through flood water. Just 12 inches can sweep away a car, 2 feet can float most vehicles."
                );

            case "fire":
                return new DisasterInfo(
                    "Fire Safety",
                    "BEFORE:\n" +
                    "• Install smoke detectors on every level\n" +
                    "• Test smoke alarms monthly\n" +
                    "• Create and practice escape plan\n" +
                    "• Keep fire extinguisher accessible\n" +
                    "• Clear escape routes\n" +
                    "• Never overload electrical outlets\n" +
                    "• Keep matches away from children\n" +
                    "• Have fire blankets ready",

                    "DURING:\n" +
                    "• Alert everyone - yell 'FIRE!' loudly\n" +
                    "• Call 101 (Fire) or 112\n" +
                    "• Get out immediately - Do NOT collect valuables\n" +
                    "• Stay low - crawl under smoke\n" +
                    "• Feel doors before opening - if hot, use alternative route\n" +
                    "• Close doors behind you to slow spread\n" +
                    "• Do NOT use elevators\n" +
                    "• If clothes catch fire: STOP, DROP, and ROLL\n" +
                    "• Once out, stay out",

                    "AFTER:\n" +
                    "• Do NOT re-enter until declared safe\n" +
                    "• Contact emergency services\n" +
                    "• Take photos of damage\n" +
                    "• Contact insurance company\n" +
                    "• Seek medical attention for any injuries\n" +
                    "• Watch for structural damage",
                    "TIPS:\n" +
                    "• Practice family fire drill monthly\n" +
                    "• Know two ways out of every room\n" +
                    "• Keep keys near locked doors\n" +
                    "• Learn to use fire extinguisher\n" +
                    "• Install escape ladders for upper floors",
                    "Most fire deaths are caused by smoke inhalation, not burns. Stay low to breathe cleaner air."
                );

            case "cyclone":
                return new DisasterInfo(
                    "Cyclone Safety",
                    "BEFORE:\n" +
                    "• Know your cyclone risk area\n" +
                    "• Reinforce doors, windows, and roof\n" +
                    "• Trim trees and clear debris\n" +
                    "• Prepare emergency kit\n" +
                    "• Fill clean water containers\n" +
                    "• Charge all devices\n" +
                    "• Identify nearest cyclone shelter\n" +
                    "• Have battery-operated radio",

                    "DURING:\n" +
                    "• Stay inside away from windows\n" +
                    "• Move to strongest part of building\n" +
                    "• Do NOT go outside during eye (calm period)\n" +
                    "• Listen to emergency broadcasts\n" +
                    "• If outdoors, seek shelter immediately\n" +
                    "• Do NOT shelter under trees\n" +
                    "• If driving, stop away from trees, power lines, water\n" +
                    "• Turn off utilities if instructed",

                    "AFTER:\n" +
                    "• Wait for official all-clear before going outside\n" +
                    "• Watch for fallen power lines\n" +
                    "• Do NOT touch electrical equipment if wet\n" +
                    "• Check for structural damage before entering\n" +
                    "• Use flashlight, not candles\n" +
                    "• Document damage for insurance\n" +
                    "• Help others safely if possible",
                    "TIPS:\n" +
                    "• Never be misled by the calm eye - winds return from opposite direction after\n" +
                    "• Have adequate food and water supplies\n" +
                    "• Store essential items above potential flood level\n" +
                    "• Practice evacuation before cyclone season",
                    "The calm 'eye' of a cyclone can last 30 minutes, then winds return fiercely from the opposite direction. Do NOT go outside."
                );

            case "lightning":
                return new DisasterInfo(
                    "Lightning Safety",
                    "BEFORE:\n" +
                    "• Check weather forecasts before outdoor activities\n" +
                    "• Know the 30-30 rule: if time between flash and thunder is 30 seconds or less, seek shelter\n" +
                    "• Identify safe shelters nearby\n" +
                    "• Install lightning protection system\n" +
                    "• Unplug sensitive electronics in stormy weather\n" +
                    "• Stay away from windows during storms",

                    "DURING:\n" +
                    "• Seek shelter in substantial building or hard-topped vehicle\n" +
                    "• Avoid open areas, hilltops, tall isolated objects\n" +
                    "• Do NOT seek shelter under trees\n" +
                    "• Stay away from water, metal objects\n" +
                    "• Do NOT use corded phones\n" +
                    "• Avoid plumbing - do NOT bathe, shower, wash dishes\n" +
                    "• If no shelter: crouch low on balls of feet, minimize contact with ground\n" +
                    "• Spread out if in a group\n" +
                    "• Stay inside car with windows up",

                    "AFTER:\n" +
                    "• Wait 30 minutes after last thunder before safe to resume outdoor activity\n" +
                    "• If someone is struck, call 112 immediately\n" +
                    "• Lightning victims do NOT carry charge - safe to touch\n" +
                    "• begin CPR if not breathing\n" +
                    "• Check for burns and injuries\n" +
                    "• Monitor for shock symptoms",
                    "TIPS:\n" +
                    "• 'When thunder roars, go indoors'\n" +
                    "• If you can hear thunder, you're close enough to be struck\n" +
                    "• Lightning can strike even without rain - 'dry lightning'\n" +
                    "• Get out of and away from water immediately",
                    "Lightning is extremely dangerous. It can strike up to 10 miles away from a storm. When thunder roars, go indoors."
                );

            default:
                return new DisasterInfo(
                    "General Emergency Preparedness",
                    "BEFORE AN EMERGENCY:\n" +
                    "• Create a family emergency plan\n" +
                    "• Prepare an emergency kit\n" +
                    "• Learn first aid and CPR\n" +
                    "• Know emergency numbers (112, 108, 100, 101)\n" +
                    "• Identify meeting points\n" +
                    "• Keep important documents accessible\n" +
                    "• Practice emergency drills\n" +
                    "• Install emergency apps",

                    "DURING AN EMERGENCY:\n" +
                    "• Stay calm and think clearly\n" +
                    "• Call emergency services if needed\n" +
                    "• Follow your emergency plan\n" +
                    "• Help others if safe to do so\n" +
                    "• Stay informed through official channels\n" +
                    "• Do NOT spread rumors\n" +
                    "• Conserve battery power\n" +
                    "• Stay away from hazards\n" +
                    "• Follow evacuation orders",

                    "AFTER AN EMERGENCY:\n" +
                    "• Check for injuries and apply first aid\n" +
                    "• Call for help if needed\n" +
                    "• Document damage for insurance\n" +
                    "• Avoid hazards (fallen power lines, debris)\n" +
                    "• Stay out of damaged buildings\n" +
                    "• Follow official instructions\n" +
                    "• Help community members safely\n" +
                    "• Take care of mental health\n" +
                    "• Be patient with recovery",
                    "EMERGENCY KIT CONTENTS:\n" +
                    "• Water (1 gallon per person per day, 3 days)\n" +
                    "• Non-perishable food\n" +
                    "• First aid kit\n" +
                    "• Flashlight and extra batteries\n" +
                    "• Phone charger (battery or solar)\n" +
                    "• Important documents copies\n" +
                    "• Cash in small bills\n" +
                    "• Medications\n" +
                    "• Local maps",
                    "Being prepared can save your life and the lives of those around you. Take disaster preparedness seriously."
                );
        }
    }

    private void readAloud(String type) {
        DisasterInfo info = getDisasterInfo(type);
        if (textToSpeech != null) {
            String text = info.title + ". Before: " + info.before + ". During: " + info.during +
                ". After: " + info.after;
            textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
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

    private static class DisasterInfo {
        String title;
        String before;
        String during;
        String after;
        String tips;
        String warning;

        DisasterInfo(String title, String before, String during, String after, String tips, String warning) {
            this.title = title;
            this.before = before;
            this.during = during;
            this.after = after;
            this.tips = tips;
            this.warning = warning;
        }
    }
}
