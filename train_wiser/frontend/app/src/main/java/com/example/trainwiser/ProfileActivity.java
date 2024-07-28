package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

public class ProfileActivity extends AppCompatActivity {

    private String userId;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
    }

    @Override
    public void onSaveInstanceState(Bundle savedInstanceState) {
        super.onSaveInstanceState(savedInstanceState);
        savedInstanceState.putString("user_id", userId);
    }

    @Override
    protected void onResume() {
        super.onResume();

        String userIdIntent = getIntent().getStringExtra("user_id");
        if (userIdIntent != null && !userIdIntent.isEmpty())
            userId = userIdIntent;
    }
}
