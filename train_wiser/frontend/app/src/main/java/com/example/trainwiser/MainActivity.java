package com.example.trainwiser;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.utils.APIUtils;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    protected void onResume() {
        super.onResume();

        String accessToken = APIUtils.getAccessToken(getApplicationContext());
        String refreshToken = APIUtils.getRefreshToken(getApplicationContext());
        long expiresAt = APIUtils.getExpiresAt(getApplicationContext());
        final boolean isLoggedIn = accessToken == null || refreshToken == null || expiresAt == Long.MAX_VALUE;

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent newActivity = null;
                if (isLoggedIn) {
                    newActivity = new Intent(MainActivity.this, MainMenuActivity.class);
                } else {
                    newActivity = new Intent(MainActivity.this, LoginActivity.class);
                }
                startActivity(newActivity);
                finish();
            }
        }, 2000);
    }
}
