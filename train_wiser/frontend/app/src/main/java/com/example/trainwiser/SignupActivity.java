package com.example.trainwiser;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIInterface;
import com.example.trainwiser.network.APIRetrofitClient;
import com.example.trainwiser.network.api_models.registration.RegisterRequestData;
import com.example.trainwiser.network.api_models.registration.RegisterResponseData;

import org.json.JSONObject;

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

        // Password check
        String password = passwordEditText.getText().toString();
        String confirmPassword = confirmPasswordEditText.getText().toString();
        if (password.isEmpty()) {
            Toast.makeText(SignupActivity.this, "Password field cannot be empty", Toast.LENGTH_LONG).show();
            return;
        }
        if (confirmPassword.isEmpty()) {
            Toast.makeText(SignupActivity.this, "Confirm Password cannot be empty", Toast.LENGTH_LONG).show();
            return;
        }
        if (!password.equals(confirmPassword)) {
            Toast.makeText(SignupActivity.this, "Password and confirm password do not match", Toast.LENGTH_LONG).show();
            return;
        }

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
                    Toast.makeText(SignupActivity.this, "Error happen during sign up. Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<RegisterResponseData> call, Throwable t) {
                Utils.onFailureLogging(SignupActivity.this, t);
            }
        });
    }
}
