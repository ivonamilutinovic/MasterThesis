package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.login.LoginRequestData;
import com.example.trainwiser.network.api_models.login.LoginResponseData;
import com.example.trainwiser.network.api_models.logout.LogoutRequestData;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface Oauth2Interface {

    @POST("token/")
    Call<LoginResponseData> loginUser(@Body LoginRequestData data);

    @POST("revoke_token/")
    Call<Void> logoutUser(@Body LogoutRequestData data);
}
