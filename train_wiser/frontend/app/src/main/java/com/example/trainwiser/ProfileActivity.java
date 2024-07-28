package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

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

        populateProfileData();
    }

    public void populateProfileData() {
        ProfileSingleton profile = ProfileSingleton.getInstance();

        EditText editTextUserName = findViewById(R.id.usernameId);
        EditText editTextEmail = findViewById(R.id.userEmailId);
        EditText editTextFirstName = findViewById(R.id.usernameFirstNameId);
        EditText editTextSecondName = findViewById(R.id.usernameLastNameId);
        EditText editTextBirthDate = findViewById(R.id.usernameBirthDateId);

        editTextUserName.setText(profile.getUsername());
        editTextEmail.setText(profile.getEmail());
        editTextFirstName.setText(profile.getFirst_name());
        editTextSecondName.setText(profile.getLast_name());
        editTextBirthDate.setText(profile.getBirth_date());
    }


    public void onClickSaveChanges(View view) {

    }

    public void onDeleteAccount(View view) {

    }

}
