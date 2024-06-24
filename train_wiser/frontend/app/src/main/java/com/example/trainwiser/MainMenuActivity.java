package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainMenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_menu);

        Button buttonPT = this.findViewById(R.id.buttonPT);
        Button buttonAIPT = this.findViewById(R.id.buttonAIPT);
        Button buttonPrediction = this.findViewById(R.id.buttonPrediction);

        buttonPT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent newActivity = new Intent(MainMenuActivity.this, PersonalTrainerActivity.class);
                startActivity(newActivity);
            }
        });

        buttonAIPT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent newActivity = new Intent(MainMenuActivity.this, AIPersonalTrainerActivity.class);
                startActivity(newActivity);
            }
        });

        buttonPrediction.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent newActivity = new Intent(MainMenuActivity.this, ResultsPredictionActivity.class);
                startActivity(newActivity);
            }
        });

    }
}