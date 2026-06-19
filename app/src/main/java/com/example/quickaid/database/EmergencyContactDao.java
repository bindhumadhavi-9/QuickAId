package com.example.quickaid.database;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.example.quickaid.models.EmergencyContact;

import java.util.List;

import io.reactivex.rxjava3.core.Completable;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Single;

@Dao
public interface EmergencyContactDao {
    @Insert
    long insert(EmergencyContact contact);

    @Update
    void update(EmergencyContact contact);

    @Delete
    void delete(EmergencyContact contact);

    @Query("SELECT * FROM emergency_contact ORDER BY isFavorite DESC, name ASC")
    List<EmergencyContact> getAllContacts();

    @Query("SELECT * FROM emergency_contact WHERE isFavorite = 1 ORDER BY name ASC")
    List<EmergencyContact> getFavoriteContacts();

    @Query("SELECT * FROM emergency_contact WHERE id = :id")
    EmergencyContact getContactById(long id);

    @Query("DELETE FROM emergency_contact WHERE id = :id")
    void deleteById(long id);

    @Query("SELECT COUNT(*) FROM emergency_contact")
    int getContactCount();
}
