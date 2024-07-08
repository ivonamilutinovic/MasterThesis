package com.example.trainwiser;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIInterface;
import com.example.trainwiser.network.APIRetrofitClient;
import com.example.trainwiser.network.api_models.RegisterRequestData;
import com.example.trainwiser.network.api_models.RegisterResponseData;

import org.json.JSONObject;

import java.io.IOException;
import java.net.HttpURLConnection;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignupActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
    }

    public void onClickSignUp(View view) {
        EditText usernameEditText = this.findViewById(R.id.usernameId);
        EditText userEmailEditText = this.findViewById(R.id.userEmailId);
        EditText usernameFirstNameEditText = this.findViewById(R.id.usernameFirstNameId);
        EditText usernameLastNameEditText = this.findViewById(R.id.usernameLastNameId);
        EditText passwordEditText = this.findViewById(R.id.userPasswordId);
        EditText confirmPasswordEditText = this.findViewById(R.id.userConfirmPasswordId);
        EditText birthDateEditText = this.findViewById(R.id.usernameBirthDateId);

        // todo: nullptr and confirm password / validation and datapicker
        RegisterRequestData registerRequestData = new RegisterRequestData(
                usernameEditText.getText().toString(),
                userEmailEditText.getText().toString(),
                usernameFirstNameEditText.getText().toString(),
                usernameLastNameEditText.getText().toString(),
                passwordEditText.getText().toString(),
                birthDateEditText.getText().toString());

        APIRetrofitClient.getAPIClient().create(APIInterface.class).registerUser(registerRequestData).enqueue(new Callback<RegisterResponseData>() {
            @Override
            public void onResponse(Call<RegisterResponseData> call, Response<RegisterResponseData> response) {
                if (response.code() == HttpURLConnection.HTTP_CREATED) {
//                    assert response.body() != null;
//                    Toast.makeText(SignupActivity.this, Integer.toString(response.body().getUser_id()), Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(SignupActivity.this, LoginActivity.class);
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

                    Toast.makeText(SignupActivity.this, "Error happen during sign up of the user. Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<RegisterResponseData> call, Throwable t) {

            }
        });
    }
}
