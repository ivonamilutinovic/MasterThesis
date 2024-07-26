package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.LoginRequestData;
import com.example.trainwiser.network.api_models.LoginResponseData;
import com.example.trainwiser.network.api_models.RegisterRequestData;

import retrofit2.Call;
import retrofit2.Response;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface Oauth2Interface {

    @POST("token/")
    Call<LoginResponseData> loginUser(@Body LoginRequestData data);

    @POST("revoke_token/")
    Call<Response<Void>> logoutUser(@Body RegisterRequestData data);
}
