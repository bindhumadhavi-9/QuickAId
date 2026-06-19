package com.example.quickaid.database;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.example.quickaid.models.FirstAidItem;

import java.util.List;

@Dao
public interface FirstAidItemDao {
    @Insert
    long insert(FirstAidItem item);

    @Update
    void update(FirstAidItem item);

    @Delete
    void delete(FirstAidItem item);

    @Query("SELECT * FROM FirstAidItem ORDER BY itemName ASC")
    List<FirstAidItem> getAllItems();

    @Query("SELECT * FROM FirstAidItem WHERE isAvailable = 1 ORDER BY itemName ASC")
    List<FirstAidItem> getAvailableItems();

    @Query("SELECT * FROM FirstAidItem WHERE isAvailable = 0 ORDER BY itemName ASC")
    List<FirstAidItem> getMissingItems();

    @Query("SELECT COUNT(*) FROM FirstAidItem WHERE isAvailable = 1")
    int getAvailableCount();

    @Query("SELECT COUNT(*) FROM FirstAidItem")
    int getTotalCount();

    @Query("DELETE FROM FirstAidItem WHERE id = :id")
    void deleteById(long id);
}
