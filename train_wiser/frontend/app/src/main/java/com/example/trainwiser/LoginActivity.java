package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        Button logInButton = this.findViewById(R.id.logInId);
        EditText userEmailEditText = this.findViewById(R.id.userEmailId);
        EditText userPasswordEditText = this.findViewById(R.id.userPasswordId);
        TextView signUpTextView = this.findViewById(R.id.signUpTextId);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    public void onLogInClick(View view)
    {
        btnSignIn.setEnabled(false);

        String email = etEmail.getText().toString();
        String password = etPassword.getText().toString();

        Context thisActivity = this;

        APIWrapper.GetAccessToken(getApplicationContext(), email, password, new AbstractAPIResponseHandler() {
            @Override
            public void Handle(JSONObject response, int statusCode) throws JSONException {
                switch(statusCode)
                {
                    case HttpURLConnection.HTTP_OK:
                        String access_token = response.getString("access_token");
                        String refresh_token = response.getString("refresh_token");
                        long expires_in = response.getLong("expires_in");

                        APIWrapper.SaveAuthorizationParams(getApplicationContext(), access_token, refresh_token, expires_in);

                        // redirect to profile
                        Intent intent = new Intent(thisActivity, ProfileActivity.class);
                        intent.putExtra("user_id", "me");

                        thisActivity.startActivity(intent);
                        break;
                    case HttpURLConnection.HTTP_UNAUTHORIZED:
                        Toast.makeText(getApplicationContext(), "Unexpected error", Toast.LENGTH_LONG).show();
                        break;
                    case HttpURLConnection.HTTP_BAD_REQUEST:
                        Toast.makeText(getApplicationContext(), "Wrong email or password", Toast.LENGTH_LONG).show();
                        break;
                    default:
                        Toast.makeText(getApplicationContext(), "Internal error", Toast.LENGTH_LONG).show();
                        break;
                }

                btnSignIn.setEnabled(true);
            }
        });
    }
}