package com.example.trainwiser;


import android.os.Handler;
import android.os.Looper;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.trainwiser.network.APIClientWithInterceptorForTokens;
import com.example.trainwiser.network.APIInterfaceWithInterceptorForTokens;
import com.example.trainwiser.network.api_models.account.AccountDataResponse;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ProfileSingleton {

    private static ProfileSingleton instance;

    private Integer strava_athlete_id; // 121978
    private String username;
    private String email;
    private String first_name;
    private String last_name;
    private String birth_date;

    private ProfileSingleton() {}

    public ProfileSingleton(Integer strava_id, String username, String email, String first_name, String second_name, String birth_date) {
        this.strava_athlete_id = strava_id;
        this.username = username;
        this.email = email;
        this.first_name = first_name;
        this.last_name = second_name;
        this.birth_date = birth_date;
    }

    public static synchronized ProfileSingleton getInstance() {
        if (instance == null) {
            instance = new ProfileSingleton();
        }
        return instance;
    }

    public boolean isUserConnectedWithStrava() {
        return strava_athlete_id != null;
    }

    public static void setInstance(ProfileSingleton instance) {
        ProfileSingleton.instance = instance;
    }

    public Integer getStrava_athlete_id() {
        return strava_athlete_id;
    }

    public void setStrava_athlete_id(Integer strava_athlete_id) {
        this.strava_athlete_id = strava_athlete_id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirst_name() {
        return first_name;
    }

    public void setFirst_name(String first_name) {
        this.first_name = first_name;
    }

    public String getLast_name() {
        return last_name;
    }

    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    public String getBirth_date() {
        return birth_date;
    }

    public void setBirth_date(String birth_date) {
        this.birth_date = birth_date;
    }

    public void renderProfileData(AppCompatActivity activity, Runnable callbackFunction){
        APIClientWithInterceptorForTokens.getAPIClient(activity).create(APIInterfaceWithInterceptorForTokens.class)
                .getAccount().enqueue(new Callback<AccountDataResponse>() {
            @Override
            public void onResponse(Call<AccountDataResponse> call, Response<AccountDataResponse> response) {
                if (response.isSuccessful()) {
                    AccountDataResponse accountData = response.body();
                    first_name = accountData.getFirst_name();
                    last_name = accountData.getLast_name();
                    email = accountData.getEmail();
                    username = accountData.getUsername();
                    birth_date = accountData.getBirth_date();
                    strava_athlete_id = accountData.getStrava_athlete_id();
                    Handler mainHandler = new Handler(Looper.getMainLooper());
                    mainHandler.post(callbackFunction);
                }
                else{
                    ResponseBody errorBody = response.errorBody();
                    String errorText = "Unknown error";
                    if (errorBody != null){
                        try {
                            errorText = errorBody.string();
                        } catch (Exception ignored) {
                        }
                    }
                    Toast.makeText(activity, "Error code: " + response.code() + " (" + errorText + ")", Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<AccountDataResponse> call, Throwable t) {
                Utils.onFailureLogging(activity, t);
            }
        });
    }

    public void emptyProfileData() {
        this.strava_athlete_id = null;
        this.username = null;
        this.email = null;
        this.first_name = null;
        this.last_name = null;
        this.birth_date = null;
    }
 }

