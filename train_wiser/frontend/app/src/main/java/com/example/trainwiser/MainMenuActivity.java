package com.example.trainwiser;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.common.GlobalAPIAccessData;
import com.example.trainwiser.network.Oauth2Interface;
import com.example.trainwiser.network.Oauth2RetrofitClient;
import com.example.trainwiser.network.api_models.logout.LogoutRequestData;
import com.example.trainwiser.network.utils.APIUtils;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainMenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_menu);
    }

    @Override
    protected void onResume() {
        super.onResume();
        setContentView(R.layout.activity_main_menu);

        Button stravaConnectionButton = findViewById(R.id.buttonConnectWithStrava);
        ProfileSingleton profile = ProfileSingleton.getInstance();

        if (profile.isUserConnectedWithStrava()) {
            stravaConnectionButton.setText(R.string.strava_account_connected);
            stravaConnectionButton.setClickable(false);
            stravaConnectionButton.setBackgroundColor(getResources().getColor(R.color.negative_option_for_buttons, getTheme()));
            stravaConnectionButton.setTextColor(getResources().getColor(R.color.for_text_on_negative_buttons, getTheme()));
        } else {
            stravaConnectionButton.setText(R.string.connect_with_strava);
            stravaConnectionButton.setBackgroundColor(getResources().getColor(R.color.for_buttons, getTheme()));
            stravaConnectionButton.setTextColor(getResources().getColor(R.color.for_text_on_buttons, getTheme()));
        }
    }

    public void onClickSwitchToTrainingSuggestions(View view) {
        Intent intent = new Intent(MainMenuActivity.this, TrainingsPlansActivity.class);
        startActivity(intent);
    }

    public void onClickSwitchToResultsPredictionScreen(View view) {
        Intent intent = new Intent(MainMenuActivity.this, ResultsPredictActivity.class);
        startActivity(intent);
    }

    public void onClickSwitchToTrainingStats(View view) {
        Intent intent = new Intent(MainMenuActivity.this, TrainingStatsActivity.class);
        startActivity(intent);
    }

    private void switchToProfileActivity() {
        Intent intent = new Intent(MainMenuActivity.this, ProfileActivity.class);
        startActivity(intent);
    }

    public void onClickProfile(View view) {
        ProfileSingleton profile = ProfileSingleton.getInstance();
        profile.renderProfileData(MainMenuActivity.this,  new Runnable() {
            @Override
            public void run() {
                switchToProfileActivity();
            }
        });
    }

    public void onClickStravaConnection(View view) {
        Button button = findViewById(R.id.buttonConnectWithStrava);
        ProfileSingleton profile = ProfileSingleton.getInstance();

        if (!profile.isUserConnectedWithStrava()) {
            String stravaAuthorizationURL = GlobalAPIAccessData.getStravaAuthorizationURL();
            if (stravaAuthorizationURL != null) {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(stravaAuthorizationURL));
                MainMenuActivity.this.startActivity(intent);

                profile.renderProfileData(MainMenuActivity.this, null);
                Integer stravaAthleteId = profile.getStrava_athlete_id();
                if(stravaAthleteId != null) {
                    button.setText(R.string.strava_account_connected);
                    button.setClickable(false);
                    button.setBackgroundColor(getResources().getColor(R.color.negative_option_for_buttons, getTheme()));
                    button.setTextColor(getResources().getColor(R.color.for_text_on_negative_buttons, getTheme()));
                }
            } else {
                Toast.makeText(MainMenuActivity.this, "Error during Strava authorization", Toast.LENGTH_LONG).show();
            }
        }
    }

    public void getTrainingPlansRequest(){
        String token = APIUtils.getAccessToken(getApplicationContext());
        LogoutRequestData logoutRequestData = new LogoutRequestData(
                GlobalAPIAccessData.getClientId(),
                GlobalAPIAccessData.getClientSecret(),
                token);

        Oauth2RetrofitClient.getOauth2Client().create(Oauth2Interface.class).logoutUser(logoutRequestData).enqueue(new Callback<Void>() {
            private void logout_user() {
                APIUtils.removeAPIKeysData(getApplicationContext());
                ProfileSingleton.getInstance().emptyProfileData();
                Intent intent = new Intent(MainMenuActivity.this, LoginActivity.class);
                startActivity(intent);
                finish();
            }
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                logout_user();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Utils.onFailureLogging(MainMenuActivity.this, t);
                logout_user();
            }
        });
    }

    public void onClickLogout(View view) {
        APIUtils.refreshAccessTokenIfNeeded(MainMenuActivity.this,  new Runnable() {
            @Override
            public void run() {
                getTrainingPlansRequest();
            }
        });

    }

}