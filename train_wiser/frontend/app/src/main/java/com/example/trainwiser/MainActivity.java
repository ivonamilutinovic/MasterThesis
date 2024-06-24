package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    private Button buttonPT;
    private Button buttonAIPT;
    private Button buttonPrediction;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final boolean isLoggedIn = true;  // todo: replace with method
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent newActivity = null;
                if(isLoggedIn){
                    newActivity = new Intent(MainActivity.this, LoginActivity.class);
                }else{
                    newActivity = new Intent(MainActivity.this, MainMenuActivity.class);
                }
                startActivity(newActivity);
                finish();
            }
        }, 2000);
    }
}
