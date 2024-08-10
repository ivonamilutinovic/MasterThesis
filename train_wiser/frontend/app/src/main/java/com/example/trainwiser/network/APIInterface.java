package com.example.trainwiser.network;

import com.example.trainwiser.network.api_models.registration.RegisterRequestData;
import com.example.trainwiser.network.api_models.registration.RegisterResponseData;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface APIInterface {
    @POST("users/register/")
    Call<RegisterResponseData> registerUser(@Body RegisterRequestData user);

//    @GET("account/{username}/")
//    Call<AccountDataResponse> getAccount(@Path("username") String username);

//    @PATCH("account/{username}/")
//    Call<AccountDataResponse> updateAccount(@Path("username") String username, @Body AccountDataRequest account);

}
