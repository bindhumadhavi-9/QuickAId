package com.example.quickaid;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    Button btnEmergency, btnBodyGuide, btnTips, btnSOS, btnKit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnEmergency = findViewById(R.id.btnEmergency);
        btnBodyGuide = findViewById(R.id.btnBodyGuide);
        btnTips = findViewById(R.id.btnTips);
        btnSOS = findViewById(R.id.btnSOS);
        btnKit = findViewById(R.id.btnKit);

        btnEmergency.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, EmergencyActivity.class);
            startActivity(intent);
        });

        btnBodyGuide.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, BodyGuideActivity.class);
            startActivity(intent);
        });

        btnTips.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, TipsActivity.class);
            startActivity(intent);
        });

        btnSOS.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, ContactsActivity.class);
            startActivity(intent);
        });

        btnKit.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, FirstAidKitActivity.class);
            startActivity(intent);
        });
    }
}