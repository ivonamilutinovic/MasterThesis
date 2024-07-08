package com.example.trainwiser;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

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
        Button logInButton = this.findViewById(R.id.logInId);
        EditText usernameEditText = this.findViewById(R.id.usernameId);
        EditText userPasswordEditText = this.findViewById(R.id.userPasswordId);
        TextView signUpTextView = this.findViewById(R.id.signUpTextId);

        // link for connection with strava: https://www.strava.com/api/v3/oauth/authorize?response_type=code&client_id=121978&redirect_uri=https://feasible-brightly-cobra.ngrok-free.app/stava_gateway/token_exchange/&scope=profile%3Aread_all%20read%20activity%3Aread_all
        // oauth2 ka backendu
    }

}
