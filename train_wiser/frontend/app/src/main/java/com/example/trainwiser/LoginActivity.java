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

        Button logInButton = this.findViewById(R.id.logInId);
        EditText userEmailEditText = this.findViewById(R.id.userEmailId);
        EditText userPasswordEditText = this.findViewById(R.id.userPasswordId);
        TextView signUpTextView = this.findViewById(R.id.signUpTextId);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }
    
}