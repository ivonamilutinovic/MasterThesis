package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class MainMenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_menu);

    }

    public void onClickSwitchPersonalTrainerScreen(View view) {
        Intent intent = new Intent(MainMenuActivity.this, PersonalTrainerActivity.class);
        startActivity(intent);
    }

    public void onClickSwitchToAIPersonalTrainerScreen(View view) {
        Intent intent = new Intent(MainMenuActivity.this, AIPersonalTrainerActivity.class);
        startActivity(intent);
    }

    public void onClickSwitchResultsPredictionScreen(View view) {
        Intent intent = new Intent(MainMenuActivity.this, ResultsPredictionActivity.class);
        startActivity(intent);
    }

    public void onClickSwitchResultsPredictionScreen(View view) {
        Intent intent = new Intent(MainMenuActivity.this, ResultsPredictionActivity.class);
        startActivity(intent);
    }

    public void onClickSwitchResultsPredictionScreen(View view) {
        Intent intent = new Intent(MainMenuActivity.this, ResultsPredictionActivity.class);
        startActivity(intent);
    }

    public void onClickLogout(View view) {
        Toast.makeText(MainMenuActivity.this, "User is logged out", Toast.LENGTH_LONG).show();
    }
}