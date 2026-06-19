package com.example.quickaid.models;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "first_aid_item")
public class FirstAidItem {
    @PrimaryKey(autoGenerate = true)
    private long id;
    private String itemName;
    private int quantity;
    private boolean isAvailable;
    private String notes;
    private long lastChecked;

    public FirstAidItem() {}

    public FirstAidItem(String itemName, int quantity, boolean isAvailable) {
        this.itemName = itemName;
        this.quantity = quantity;
        this.isAvailable = isAvailable;
    }

    public FirstAidItem(String itemName, String description, int quantity, boolean isAvailable) {
        this.itemName = itemName;
        this.quantity = quantity;
        this.isAvailable = isAvailable;
        this.notes = description;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getItemName() {
        return itemName;
    }

    public void setItemName(String itemName) {
        this.itemName = itemName;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public boolean isAvailable() {
        return isAvailable;
    }

    public void setAvailable(boolean available) {
        isAvailable = available;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }

    public long getLastChecked() {
        return lastChecked;
    }

    public void setLastChecked(long lastChecked) {
        this.lastChecked = lastChecked;
    }
}
