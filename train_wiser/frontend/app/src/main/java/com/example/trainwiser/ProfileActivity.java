package com.example.trainwiser;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIClientWithInterceptorForTokens;
import com.example.trainwiser.network.APIInterfaceWithInterceptorForTokens;
import com.example.trainwiser.network.api_models.account.AccountDataResponse;
import com.example.trainwiser.network.utils.APIUtils;

import java.util.HashMap;
import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ProfileActivity extends AppCompatActivity {

    private String userId;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
    }

    @Override
    public void onSaveInstanceState(Bundle savedInstanceState) {
        super.onSaveInstanceState(savedInstanceState);
        savedInstanceState.putString("user_id", userId);
    }

    @Override
    protected void onResume() {
        super.onResume();

        String userIdIntent = getIntent().getStringExtra("user_id");
        if (userIdIntent != null && !userIdIntent.isEmpty())
            userId = userIdIntent;

        populateProfileData();
    }

    public void populateProfileData() {
        ProfileSingleton profile = ProfileSingleton.getInstance();

        EditText editTextUserName = findViewById(R.id.profileUsernameId);
        EditText editTextEmail = findViewById(R.id.profileEmailId);
        EditText editTextFirstName = findViewById(R.id.profileFirstNameId);
        EditText editTextLastName = findViewById(R.id.profileLastNameId);
        EditText editTextBirthDate = findViewById(R.id.profileBirthDateId);

        editTextUserName.setText(profile.getUsername());
        editTextEmail.setText(profile.getEmail());
        editTextFirstName.setText(profile.getFirst_name());
        editTextLastName.setText(profile.getLast_name());
        editTextBirthDate.setText(profile.getBirth_date());
    }

    private Map<String, Object> getUpdatedFields(ProfileSingleton profile) {

        EditText editTextUserName = findViewById(R.id.profileUsernameId);
        EditText editTextEmail = findViewById(R.id.profileEmailId);
        EditText editTextPassword = findViewById(R.id.profilePasswordId);
        EditText editTextFirstName = findViewById(R.id.profileFirstNameId);
        EditText editTextLastName = findViewById(R.id.profileLastNameId);
        EditText editTextBirthDate = findViewById(R.id.profileBirthDateId);
        Map<String, Object> profileUpdates = new HashMap<>();

        String newUsername = editTextUserName.getText().toString();
        if (!newUsername.equals(profile.getUsername())) {
            profileUpdates.put("username", newUsername);
        }

        String newEmail = editTextEmail.getText().toString();
        if (!newEmail.equals(profile.getEmail())) {
            profileUpdates.put("email", newEmail);
        }

        String newPassword = editTextPassword.getText().toString();
        if (!newPassword.equals("********")) {
            profileUpdates.put("password", newPassword);
        }

        String newFirstName = editTextFirstName.getText().toString();
        if (!newFirstName.equals(profile.getFirst_name())) {
            profileUpdates.put("first_name", newFirstName);
        }

        String newLastName = editTextLastName.getText().toString();
        if (!newLastName.equals(profile.getLast_name())) {
            profileUpdates.put("last_name", newLastName);
        }

        String newBirthDate = editTextBirthDate.getText().toString();
        if (!newBirthDate.equals(profile.getBirth_date())) {
            profileUpdates.put("birth_date", newBirthDate);
        }

        return profileUpdates;
    }

    public void onClickSaveChanges(View view) {
        ProfileSingleton profile = ProfileSingleton.getInstance();
        Map<String, Object> profileUpdates = getUpdatedFields(profile);

        APIClientWithInterceptorForTokens.getAPIClient(ProfileActivity.this).create(APIInterfaceWithInterceptorForTokens.class)
                .updateAccount(profileUpdates).enqueue(new Callback<AccountDataResponse>() {
                    @Override
                    public void onResponse(Call<AccountDataResponse> call, Response<AccountDataResponse> response) {
                        if (response.isSuccessful()) {
                            AccountDataResponse accountData = response.body();
                            profile.setFirst_name(accountData.getFirst_name());
                            profile.setLast_name(accountData.getLast_name());
                            profile.setEmail(accountData.getEmail());
                            profile.setUsername(accountData.getUsername());
                            profile.setStrava_athlete_id(accountData.getStrava_athlete_id());

                            Toast.makeText(ProfileActivity.this, "Profile data successfully changed.",
                                    Toast.LENGTH_LONG).show();

                            Intent intent = new Intent(ProfileActivity.this, MainMenuActivity.class);
                            startActivity(intent);
                        }
                        else{
                            Utils.onResponseErrorLogging(ProfileActivity.this, response);
                        }
                    }

                    @Override
                    public void onFailure(Call<AccountDataResponse> call, Throwable t) {
                        Utils.onFailureLogging(ProfileActivity.this, t);
                    }
                });
    }

    public void onDeleteAccount(View view) {
        APIClientWithInterceptorForTokens.getAPIClient(ProfileActivity.this)
                .create(APIInterfaceWithInterceptorForTokens.class)
                .deleteAccount().enqueue(new Callback<Void>() {
                    private void delete_user_account() {
                        APIUtils.removeAPIKeysData(getApplicationContext());
                        ProfileSingleton.getInstance().emptyProfileData();
                        Intent intent = new Intent(ProfileActivity.this, LoginActivity.class);
                        startActivity(intent);
                        finish();
                    }
                    @Override
                    public void onResponse(Call<Void> call, Response<Void> response) {
                        delete_user_account();
                    }

                    @Override
                    public void onFailure(Call<Void> call, Throwable t) {
                        Utils.onFailureLogging(ProfileActivity.this, t);
                        delete_user_account();
                    }
                });
    }

}
