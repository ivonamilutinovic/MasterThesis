package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.trainwiser.network.APIInterface;
import com.example.trainwiser.network.APIRetrofitClient;
import com.example.trainwiser.network.Oauth2Interface;
import com.example.trainwiser.network.Oauth2RetrofitClient;
import com.example.trainwiser.network.api_models.LoginRequestData;
import com.example.trainwiser.network.api_models.LoginResponseData;
import com.example.trainwiser.network.api_models.RegisterRequestData;
import com.example.trainwiser.network.api_models.RegisterResponseData;

import org.json.JSONObject;

import java.net.HttpURLConnection;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    public void onClickSwitchToSignUp(View view) {
        Intent intent = new Intent(LoginActivity.this, SignupActivity.class);
        startActivity(intent);
    }

    public void onClickLogIn(View view) {
        EditText usernameEditText = this.findViewById(R.id.usernameId);
        EditText passwordEditText = this.findViewById(R.id.userPasswordId);

        String grant_type = "password";
        LoginRequestData loginRequestData = new LoginRequestData(
                usernameEditText.getText().toString(),
                passwordEditText.getText().toString(),
                GlobalData.getClientId(),
                GlobalData.getClientSecret(),
                grant_type);

        Oauth2RetrofitClient.getOauth2Client().create(Oauth2Interface.class).loginUser(loginRequestData).enqueue(new Callback<LoginResponseData>() {
            @Override
            public void onResponse(Call<LoginResponseData> call, Response<LoginResponseData> response) {
                if (response.code() == HttpURLConnection.HTTP_OK) {
//                    assert response.body() != null;
//                    Toast.makeText(SignupActivity.this, Integer.toString(response.body().getUser_id()), Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(LoginActivity.this, MainMenuActivity.class);
                    startActivity(intent);
                }
                else{
                    ResponseBody errorBody = response.errorBody();
                    String errorText = "Unknown error";
                    if (errorBody != null){
                        try {
                            String errorBodyStr = errorBody.string();
                            JSONObject errorBodyJson = new JSONObject(errorBodyStr);

                            errorText = errorBodyJson.optString("error", errorText);
                        } catch (Exception ignored) {

                        }
                    }

                    Toast.makeText(LoginActivity.this, "Error happen during login. Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<LoginResponseData> call, Throwable t) {

            }
        });

        // oauth2 ka backendu
    }

    // link for connection with strava: https://www.strava.com/api/v3/oauth/authorize?response_type=code&client_id=121978&redirect_uri=https://feasible-brightly-cobra.ngrok-free.app/stava_gateway/token_exchange/&scope=profile%3Aread_all%20read%20activity%3Aread_all


}
