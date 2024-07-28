package com.example.trainwiser;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.common.GlobalData;
import com.example.trainwiser.network.Oauth2Interface;
import com.example.trainwiser.network.Oauth2RetrofitClient;
import com.example.trainwiser.network.api_models.LogoutRequestData;
import com.example.trainwiser.network.utils.APIUtils;

import org.json.JSONObject;

import java.net.HttpURLConnection;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

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

    public void onClickProfile(View view) {
        // link for connection with strava: https://www.strava.com/api/v3/oauth/authorize?response_type=code&client_id=121978&redirect_uri=https://feasible-brightly-cobra.ngrok-free.app/stava_gateway/token_exchange/&scope=profile%3Aread_all%20read%20activity%3Aread_all

        Intent intent = new Intent(MainMenuActivity.this, ResultsPredictionActivity.class);
        startActivity(intent);

    }

    public void onClickConnectWithStrava(View view) {
        Intent intent = new Intent(MainMenuActivity.this, ResultsPredictionActivity.class);
        startActivity(intent);
    }

    public void onClickLogout(View view) {
        String token = APIUtils.getAccessToken(getApplicationContext());
        LogoutRequestData logoutRequestData = new LogoutRequestData(
                GlobalData.getClientId(),
                GlobalData.getClientSecret(),
                token);

        Oauth2RetrofitClient.getOauth2Client().create(Oauth2Interface.class).logoutUser(logoutRequestData).enqueue(new Callback<Void>() {
            private void logout_user() {
                APIUtils.removeAPIKeysData(getApplicationContext());
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
                logout_user();
            }
        });

    }

}