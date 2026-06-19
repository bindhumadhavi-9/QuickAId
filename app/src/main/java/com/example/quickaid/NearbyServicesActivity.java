package com.example.quickaid;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.ProgressBar;

import androidx.appcompat.app.AppCompatActivity;

public class NearbyServicesActivity extends AppCompatActivity {

    private ProgressBar progressBar;

    private final String[] serviceTypes = {
        "Hospital", "Clinic", "Pharmacy", "Police Station", "Fire Station"
    };

    private final String[] serviceKeywords = {
        "hospital emergency near me",
        "medical clinic near me",
        "pharmacy near me",
        "police station near me",
        "fire station near me"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nearby_services);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Nearby Emergency Services");
        }

        initViews();
        setupServiceButtons();
    }

    private void initViews() {
        progressBar = findViewById(R.id.progressBar);
    }

    private void setupServiceButtons() {
        GridLayout gridLayout = findViewById(R.id.gridLayoutServices);
        int[] icons = {R.drawable.ic_launcher_background, R.drawable.ic_launcher_background,
                       R.drawable.ic_launcher_background, R.drawable.ic_launcher_background,
                       R.drawable.ic_launcher_background};

        for (int i = 0; i < serviceTypes.length; i++) {
            Button btn = new Button(this);
            btn.setText(serviceTypes[i]);
            btn.setTextColor(getColor(R.color.text_dark));
            btn.setBackgroundColor(getColor(R.color.white));
            btn.setTextSize(12);
            btn.setAllCaps(false);
            btn.setPadding(24, 24, 24, 24);

            int index = i;
            btn.setOnClickListener(v -> openGoogleMapsSearch(serviceKeywords[index]));

            GridLayout.LayoutParams params = new GridLayout.LayoutParams();
            params.width = 0;
            params.height = GridLayout.LayoutParams.WRAP_CONTENT;
            params.columnSpec = GridLayout.spec(i % 2, 1, 1f);
            params.setMargins(8, 8, 8, 8);
            btn.setLayoutParams(params);
            gridLayout.addView(btn);
        }
    }

    private void openGoogleMapsSearch(String keyword) {
        progressBar.setVisibility(View.VISIBLE);
        try {
            String url = "geo:0,0?q=" + Uri.encode(keyword);
            Uri gmmIntentUri = Uri.parse(url);
            Intent mapIntent = new Intent(Intent.ACTION_VIEW, gmmIntentUri);
            mapIntent.setPackage("com.google.android.apps.maps");
            startActivity(mapIntent);
        } catch (Exception e) {
            String url = "https://www.google.com/maps/search/" + Uri.encode(keyword);
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        }
        progressBar.setVisibility(View.GONE);
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}
