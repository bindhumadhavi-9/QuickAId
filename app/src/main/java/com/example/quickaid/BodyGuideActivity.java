package com.example.quickaid;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class BodyGuideActivity extends AppCompatActivity {

    Button btnHead, btnFire, btnRoad, btnWater;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_body_guide);

        btnHead = findViewById(R.id.btnHead);
        btnFire = findViewById(R.id.btnFire);
        btnRoad = findViewById(R.id.btnRoad);
        btnWater = findViewById(R.id.btnWater);

        btnHead.setOnClickListener(v -> {
            Intent intent = new Intent(BodyGuideActivity.this, HeadSafetyActivity.class);
            startActivity(intent);
        });

        btnFire.setOnClickListener(v -> {
            Intent intent = new Intent(BodyGuideActivity.this, FireSafetyActivity.class);
            startActivity(intent);
        });

        btnRoad.setOnClickListener(v -> {
            Intent intent = new Intent(BodyGuideActivity.this, RoadSafetyActivity.class);
            startActivity(intent);
        });

        btnWater.setOnClickListener(v -> {
            Intent intent = new Intent(BodyGuideActivity.this, WaterSafetyActivity.class);
            startActivity(intent);
        });
    }
}