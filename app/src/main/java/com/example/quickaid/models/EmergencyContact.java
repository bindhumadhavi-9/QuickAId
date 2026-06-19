package com.example.quickaid.models;

import androidx.annotation.NonNull;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "emergency_contact")
public class EmergencyContact {
    @PrimaryKey(autoGenerate = true)
    private long id;
    private String name;
    private String relationship;
    private String phone;
    private boolean isFavorite;

    public EmergencyContact() {}

    public EmergencyContact(String name, String relationship, String phone) {
        this.name = name;
        this.relationship = relationship;
        this.phone = phone;
        this.isFavorite = false;
    }

    public EmergencyContact(String name, String relationship, String phone, boolean isFavorite) {
        this.name = name;
        this.relationship = relationship;
        this.phone = phone;
        this.isFavorite = isFavorite;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRelationship() {
        return relationship;
    }

    public void setRelationship(String relationship) {
        this.relationship = relationship;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public boolean isFavorite() {
        return isFavorite;
    }

    public void setFavorite(boolean favorite) {
        isFavorite = favorite;
    }

    @NonNull
    @Override
    public String toString() {
        return name + " (" + relationship + ")";
    }
}
