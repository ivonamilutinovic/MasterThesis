package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.example.trainwiser.common.GlobalAPIAccessData;
import com.example.trainwiser.common.PreferenceType;
import com.example.trainwiser.common.SharedPreferenceSingleton;
import com.example.trainwiser.network.Oauth2Interface;
import com.example.trainwiser.network.Oauth2RetrofitClient;
import com.example.trainwiser.network.api_models.login.LoginRequestData;
import com.example.trainwiser.network.api_models.login.LoginResponseData;
import com.example.trainwiser.network.utils.APIKeys;
import com.example.trainwiser.network.utils.APIUtils;

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
                GlobalAPIAccessData.getClientId(),
                GlobalAPIAccessData.getClientSecret(),
                grant_type);

//        String accessToken = APIUtils.getAccessToken(getApplicationContext());
//        String refreshToken = APIUtils.getRefreshToken(getApplicationContext());
//        long expiresAt = APIUtils.getExpiresAt(getApplicationContext());

        Oauth2RetrofitClient.getOauth2Client().create(Oauth2Interface.class).loginUser(loginRequestData).enqueue(new Callback<LoginResponseData>() {
            @Override
            public void onResponse(Call<LoginResponseData> call, Response<LoginResponseData> response) {
                if (response.code() == HttpURLConnection.HTTP_OK) {
//                    assert response.body() != null;
//                    Toast.makeText(SignupActivity.this, Integer.toString(response.body().getUser_id()), Toast.LENGTH_SHORT).show();

                    if (response.body() != null) {
                        String access_token = response.body().getAccess_token();
                        long expires_in = response.body().getExpires_in();
                        String refresh_token = response.body().getRefresh_token();

                        SharedPreferenceSingleton sharedPreference = SharedPreferenceSingleton.getInstance(LoginActivity.this);
                        sharedPreference.setValue(APIKeys.API_ACCESS_TOKEN.toString(), access_token, PreferenceType.STRING);
                        sharedPreference.setValue(APIKeys.API_EXPIRES_AT.toString(), expires_in, PreferenceType.LONG);
                        sharedPreference.setValue(APIKeys.API_REFRESH_TOKEN.toString(), refresh_token, PreferenceType.STRING);

                        Intent intent = new Intent(LoginActivity.this, MainMenuActivity.class);
                        startActivity(intent);
                    }else{
                        Toast.makeText(LoginActivity.this, "Response from the backend application is empty", Toast.LENGTH_LONG).show();
                    }
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

                    Toast.makeText(LoginActivity.this, "Error happen during login. " +
                            "Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<LoginResponseData> call, Throwable t) {

            }
        });
    }

}
