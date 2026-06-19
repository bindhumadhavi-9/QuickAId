package com.example.quickaid;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.database.AppDatabase;
import com.example.quickaid.models.EmergencyContact;
import com.example.quickaid.utils.Constants;
import com.example.quickaid.utils.PreferencesManager;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;

public class ContactsManagerActivity extends AppCompatActivity {

    private static final int CALL_PERMISSION_REQUEST = 100;
    private static final int SMS_PERMISSION_REQUEST = 101;

    private ListView listViewContacts;
    private TextView textViewEmpty;
    private AppDatabase database;
    private PreferencesManager preferencesManager;
    private List<EmergencyContact> contacts = new ArrayList<>();
    private ArrayAdapter<EmergencyContact> adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contacts_manager);

        database = AppDatabase.getDatabase(this);
        preferencesManager = new PreferencesManager(this);

        listViewContacts = findViewById(R.id.listViewContacts);
        textViewEmpty = findViewById(R.id.textViewEmpty);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Emergency Contacts");
        }

        loadContacts();
        setupClickListener();
    }

    private void loadContacts() {
        Executors.newSingleThreadExecutor().execute(() -> {
            contacts = database.emergencyContactDao().getAllContacts();
            runOnUiThread(this::updateUI);
        });
    }

    private void updateUI() {
        if (contacts.isEmpty()) {
            listViewContacts.setVisibility(View.GONE);
            textViewEmpty.setVisibility(View.VISIBLE);
            textViewEmpty.setText("No emergency contacts added.\nTap + to add contacts.");
        } else {
            listViewContacts.setVisibility(View.VISIBLE);
            textViewEmpty.setVisibility(View.GONE);
            adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, contacts);
            listViewContacts.setAdapter(adapter);
        }
    }

    private void setupClickListener() {
        listViewContacts.setOnItemClickListener((parent, view, position, id) -> {
            EmergencyContact contact = contacts.get(position);
            showContactOptionsDialog(contact);
        });

        listViewContacts.setOnItemLongClickListener((parent, view, position, id) -> {
            EmergencyContact contact = contacts.get(position);
            showContactEditDeleteDialog(contact);
            return true;
        });
    }

    private void showContactOptionsDialog(EmergencyContact contact) {
        String[] options = {"Call " + contact.getName(), "Send SMS Alert", "Add to Favorites", "Cancel"};
        boolean isFavorite = contact.isFavorite();
        options[2] = isFavorite ? "Remove from Favorites" : "Add to Favorites";

        new AlertDialog.Builder(this)
            .setTitle(contact.getName() + " (" + contact.getRelationship() + ")")
            .setItems(options, (dialog, which) -> {
                switch (which) {
                    case 0: callContact(contact.getPhone()); break;
                    case 1: sendSMSToContact(contact.getPhone()); break;
                    case 2: toggleFavorite(contact); break;
                }
            })
            .show();
    }

    private void showContactEditDeleteDialog(EmergencyContact contact) {
        new AlertDialog.Builder(this)
            .setTitle("Manage Contact")
            .setItems(new String[]{"Edit", "Delete"}, (dialog, which) -> {
                if (which == 0) showEditContactDialog(contact);
                else showDeleteConfirmationDialog(contact);
            })
            .show();
    }

    private void callContact(String phone) {
        if (checkSelfPermission(Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.CALL_PHONE}, CALL_PERMISSION_REQUEST);
            return;
        }
        Intent callIntent = new Intent(Intent.ACTION_CALL);
        callIntent.setData(Uri.parse("tel:" + phone));
        startActivity(callIntent);
    }

    private void sendSMSToContact(String phone) {
        if (checkSelfPermission(Manifest.permission.SEND_SMS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.SEND_SMS}, SMS_PERMISSION_REQUEST);
            return;
        }
        String message = preferencesManager.getSosMessageTemplate();
        try {
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(phone, null, message, null, null);
            Toast.makeText(this, "Emergency SMS sent to " + phone, Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            Toast.makeText(this, "Failed to send SMS: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }

    private void sendEmergencySmsToAll() {
        if (contacts.isEmpty()) {
            Toast.makeText(this, "No contacts to send SMS to", Toast.LENGTH_SHORT).show();
            return;
        }

        new AlertDialog.Builder(this)
            .setTitle("Send Emergency SMS")
            .setMessage("This will send an emergency alert to all your saved contacts. Proceed?")
            .setPositiveButton("Send to All", (dialog, which) -> {
                if (checkSelfPermission(Manifest.permission.SEND_SMS) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.SEND_SMS}, SMS_PERMISSION_REQUEST);
                    return;
                }
                String message = preferencesManager.getSosMessageTemplate();
                int successCount = 0;
                SmsManager smsManager = SmsManager.getDefault();
                for (EmergencyContact contact : contacts) {
                    try {
                        smsManager.sendTextMessage(contact.getPhone(), null, message, null, null);
                        successCount++;
                    } catch (Exception ignored) {}
                }
                Toast.makeText(this, "Emergency SMS sent to " + successCount + " contacts",
                    Toast.LENGTH_SHORT).show();
            })
            .setNegativeButton("Cancel", null)
            .show();
    }

    private void toggleFavorite(EmergencyContact contact) {
        contact.setFavorite(!contact.isFavorite());
        Executors.newSingleThreadExecutor().execute(() -> {
            database.emergencyContactDao().update(contact);
            runOnUiThread(() -> {
                loadContacts();
                Toast.makeText(this, "Favorite status updated", Toast.LENGTH_SHORT).show();
            });
        });
    }

    private void showAddContactDialog() {
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_add_contact, null);
        EditText editTextName = dialogView.findViewById(R.id.editTextName);
        EditText editTextPhone = dialogView.findViewById(R.id.editTextPhone);
        Spinner spinnerRelationship = dialogView.findViewById(R.id.spinnerRelationship);
        editTextPhone.setInputType(android.text.InputType.TYPE_CLASS_PHONE);
        ArrayAdapter<String> spinnerAdapter = new ArrayAdapter<>(this,
            android.R.layout.simple_spinner_item, Constants.RELATIONSHIPS);
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerRelationship.setAdapter(spinnerAdapter);

        new AlertDialog.Builder(this)
            .setTitle("Add Emergency Contact")
            .setView(dialogView)
            .setPositiveButton("Add", (dialog, which) -> {
                String name = editTextName.getText().toString().trim();
                String phone = editTextPhone.getText().toString().trim();
                String relationship = spinnerRelationship.getSelectedItem().toString();

                if (name.isEmpty() || phone.isEmpty()) {
                    Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
                    return;
                }

                EmergencyContact newContact = new EmergencyContact(name, relationship, phone);
                Executors.newSingleThreadExecutor().execute(() -> {
                    database.emergencyContactDao().insert(newContact);
                    runOnUiThread(() -> {
                        loadContacts();
                        Toast.makeText(this, "Contact added", Toast.LENGTH_SHORT).show();
                    });
                });
            })
            .setNegativeButton("Cancel", null)
            .show();
    }

    private void showEditContactDialog(EmergencyContact contact) {
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_add_contact, null);
        EditText editTextName = dialogView.findViewById(R.id.editTextName);
        EditText editTextPhone = dialogView.findViewById(R.id.editTextPhone);
        Spinner spinnerRelationship = dialogView.findViewById(R.id.spinnerRelationship);

        editTextName.setText(contact.getName());
        editTextPhone.setText(contact.getPhone());
        ArrayAdapter<String> spinnerAdapter = new ArrayAdapter<>(this,
            android.R.layout.simple_spinner_item, Constants.RELATIONSHIPS);
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerRelationship.setAdapter(spinnerAdapter);

        int spinnerPos = java.util.Arrays.asList(Constants.RELATIONSHIPS).indexOf(contact.getRelationship());
        if (spinnerPos >= 0) spinnerRelationship.setSelection(spinnerPos);

        new AlertDialog.Builder(this)
            .setTitle("Edit Contact")
            .setView(dialogView)
            .setPositiveButton("Save", (dialog, which) -> {
                String name = editTextName.getText().toString().trim();
                String phone = editTextPhone.getText().toString().trim();
                String relationship = spinnerRelationship.getSelectedItem().toString();

                if (name.isEmpty() || phone.isEmpty()) {
                    Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
                    return;
                }

                contact.setName(name);
                contact.setPhone(phone);
                contact.setRelationship(relationship);

                Executors.newSingleThreadExecutor().execute(() -> {
                    database.emergencyContactDao().update(contact);
                    runOnUiThread(() -> {
                        loadContacts();
                        Toast.makeText(this, "Contact updated", Toast.LENGTH_SHORT).show();
                    });
                });
            })
            .setNegativeButton("Cancel", null)
            .show();
    }

    private void showDeleteConfirmationDialog(EmergencyContact contact) {
        new AlertDialog.Builder(this)
            .setTitle("Delete Contact")
            .setMessage("Are you sure you want to delete " + contact.getName() + "?")
            .setPositiveButton("Delete", (dialog, which) -> {
                Executors.newSingleThreadExecutor().execute(() -> {
                    database.emergencyContactDao().delete(contact);
                    runOnUiThread(() -> {
                        loadContacts();
                        Toast.makeText(this, "Contact deleted", Toast.LENGTH_SHORT).show();
                    });
                });
            })
            .setNegativeButton("Cancel", null)
            .show();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_contacts, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_add) {
            showAddContactDialog();
            return true;
        } else if (id == R.id.action_send_all) {
            sendEmergencySmsToAll();
            return true;
        } else if (id == android.R.id.home) {
            onBackPressed();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                            @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == SMS_PERMISSION_REQUEST && grantResults.length > 0
            && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "SMS permission granted. Try again.", Toast.LENGTH_SHORT).show();
        }
    }
}
