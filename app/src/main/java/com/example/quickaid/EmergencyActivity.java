package com.example.quickaid;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class EmergencyActivity extends AppCompatActivity {

    Button btnAccident;
    Button btnBurns;
    Button btnBleeding;
    Button btnElectric;
    Button btnChoking;
    Button btnFracture;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emergency);

        btnAccident = findViewById(R.id.btnAccident);
        btnBurns = findViewById(R.id.btnBurns);
        btnBleeding = findViewById(R.id.btnBleeding);
        btnElectric = findViewById(R.id.btnElectric);
        btnChoking = findViewById(R.id.btnChoking);
        btnFracture = findViewById(R.id.btnFracture);

        // Road Accident
        btnAccident.setOnClickListener(v -> {
            Intent intent = new Intent(EmergencyActivity.this, RoadActivity.class);
            startActivity(intent);
        });

        // Burns
        btnBurns.setOnClickListener(v -> {
            Intent intent = new Intent(EmergencyActivity.this, BurnsActivity.class);
            startActivity(intent);
        });

        // Bleeding
        btnBleeding.setOnClickListener(v -> {
            Intent intent = new Intent(EmergencyActivity.this, BleedingActivity.class);
            startActivity(intent);
        });

        // Electric Shock
        btnElectric.setOnClickListener(v -> {
            Intent intent = new Intent(EmergencyActivity.this, ElectricShockActivity.class);
            startActivity(intent);
        });

        // Choking
        btnChoking.setOnClickListener(v -> {
            Intent intent = new Intent(EmergencyActivity.this, ChokingActivity.class);
            startActivity(intent);
        });

        // Fracture
        btnFracture.setOnClickListener(v -> {
            Intent intent = new Intent(EmergencyActivity.this, FractureActivity.class);
            startActivity(intent);
        });
    }
}