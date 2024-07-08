package com.example.trainwiser;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final boolean isLoggedIn = false;  // todo: replace with method
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent newActivity = null;
                if(isLoggedIn){
                    newActivity = new Intent(MainActivity.this, MainMenuActivity.class);
                }else{
                    newActivity = new Intent(MainActivity.this, LoginActivity.class);
                }
                startActivity(newActivity);
                finish();
            }
        }, 2000);
    }
}
