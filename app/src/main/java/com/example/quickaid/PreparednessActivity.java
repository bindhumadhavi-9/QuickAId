package com.example.quickaid;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.models.EmergencyWorkflow;

public class PreparednessActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preparedness);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Disaster Preparedness");
        }

        setupCards();
    }

    private void setupCards() {
        findViewById(R.id.btnEarthquake).setOnClickListener(v ->
            showPreparednessInfo("earthquake"));
        findViewById(R.id.btnFlood).setOnClickListener(v ->
            showPreparednessInfo("flood"));
        findViewById(R.id.btnFire).setOnClickListener(v ->
            showPreparednessInfo("fire"));
        findViewById(R.id.btnCyclone).setOnClickListener(v ->
            showPreparednessInfo("cyclone"));
        findViewById(R.id.btnLightning).setOnClickListener(v ->
            showPreparednessInfo("lightning"));
        findViewById(R.id.btnGeneral).setOnClickListener(v ->
            showPreparednessInfo("general"));
    }

    private void showPreparednessInfo(String type) {
        android.content.Intent intent = new android.content.Intent(this, PreparednessInfoActivity.class);
        intent.putExtra("disaster_type", type);
        startActivity(intent);
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}
