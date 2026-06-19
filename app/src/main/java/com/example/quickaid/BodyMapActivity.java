package com.example.quickaid;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class BodyMapActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_body_map);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Interactive Body Guide");
        }

        setupBodyZones();
    }

    private void setupBodyZones() {
        // Front View Zones
        findViewById(R.id.zone_head).setOnClickListener(v -> showBodyPartInfo("head"));
        findViewById(R.id.zone_eyes).setOnClickListener(v -> showBodyPartInfo("eyes"));
        findViewById(R.id.zone_nose).setOnClickListener(v -> showBodyPartInfo("nose"));
        findViewById(R.id.zone_ears).setOnClickListener(v -> showBodyPartInfo("ears"));
        findViewById(R.id.zone_neck).setOnClickListener(v -> showBodyPartInfo("neck"));
        findViewById(R.id.zone_chest).setOnClickListener(v -> showBodyPartInfo("chest"));
        findViewById(R.id.zone_abdomen).setOnClickListener(v -> showBodyPartInfo("abdomen"));
        findViewById(R.id.zone_left_arm).setOnClickListener(v -> showBodyPartInfo("arm_left"));
        findViewById(R.id.zone_right_arm).setOnClickListener(v -> showBodyPartInfo("arm_right"));
        findViewById(R.id.zone_left_hand).setOnClickListener(v -> showBodyPartInfo("hand_left"));
        findViewById(R.id.zone_right_hand).setOnClickListener(v -> showBodyPartInfo("hand_right"));
        findViewById(R.id.zone_left_leg).setOnClickListener(v -> showBodyPartInfo("leg_left"));
        findViewById(R.id.zone_right_leg).setOnClickListener(v -> showBodyPartInfo("leg_right"));
        findViewById(R.id.zone_left_foot).setOnClickListener(v -> showBodyPartInfo("foot_left"));
        findViewById(R.id.zone_right_foot).setOnClickListener(v -> showBodyPartInfo("foot_right"));
    }

    private void showBodyPartInfo(String bodyPart) {
        Intent intent = new Intent(this, BodyPartInfoActivity.class);
        intent.putExtra("body_part", bodyPart);
        startActivity(intent);
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}
